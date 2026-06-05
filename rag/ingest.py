"""Ingest documents into the RAG corpus from three sources:

1. history.json (past local generations)
2. uploaded files (PDF / DOCX)
3. Jira past stories (via jira_importer)

Each function is independent and dedupes via store.exists().
"""

import os
import io
import hashlib
from typing import List, Dict, Tuple, Optional

from rag import store


# ─── 1. HISTORY ────────────────────────────────────────────────────────────

def ingest_history() -> int:
    """Index every story in history.json. Returns number of new docs added."""
    from history import load_history

    history = load_history()
    items = []
    for entry in history:
        story_text = (entry.get("story") or "").strip()
        if not story_text:
            continue
        items.append({
            "id": f"history::{entry.get('id', '')}",
            "text": story_text,
            "metadata": {
                "source": "history",
                "label": entry.get("timestamp", ""),
                "mode": entry.get("mode", ""),
            },
        })
    return store.add_many(items)


def add_to_store(entry: Dict) -> bool:
    """Live append: index a generated story entry.

    Wrapped by caller in try/except so RAG failures never break the main flow.
    """
    story_text = (entry.get("story") or "").strip()
    if not story_text:
        return False
    return store.add(
        doc_id=f"history::{entry.get('id', '')}",
        text=story_text,
        metadata={
            "source": "history",
            "label": entry.get("timestamp", ""),
            "mode": entry.get("mode", ""),
        },
    )


def add_pushed_story(story_text: str, mode: str = "pushed") -> bool:
    """Index a story that was approved by pushing it to Jira.

    Only stories the user actually pushed to Jira reach the corpus — this keeps
    the AI's memory free of rejected drafts and throwaway test runs.

    Dedupes by content hash so pushing the same story twice won't duplicate it.
    Wrapped by caller in try/except so RAG failures never break the Jira push.
    """
    text = (story_text or "").strip()
    if not text:
        return False
    content_id = hashlib.md5(text.encode("utf-8")).hexdigest()[:12]
    return store.add(
        doc_id=f"history::pushed::{content_id}",
        text=text,
        metadata={
            "source": "history",
            "label": "Jira-pushed",
            "mode": mode,
        },
    )


# ─── 2. UPLOADS (PDF / DOCX) ───────────────────────────────────────────────

def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """Split a long document into overlapping chunks for better retrieval."""
    text = (text or "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _extract_pdf(file_bytes: bytes) -> str:
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    return "\n\n".join(pages)


def _extract_docx(file_bytes: bytes) -> str:
    from docx import Document
    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return "\n".join(paragraphs)


def ingest_file(filename: str, file_bytes: bytes) -> Tuple[int, Optional[str]]:
    """Extract text from a PDF or DOCX upload, chunk it, and add to store.

    Returns (chunks_added, error_message_or_None).
    """
    name_lower = filename.lower()
    try:
        if name_lower.endswith(".pdf"):
            text = _extract_pdf(file_bytes)
        elif name_lower.endswith(".docx"):
            text = _extract_docx(file_bytes)
        else:
            return (0, f"Unsupported file type: {filename}")
    except Exception as e:
        return (0, f"Failed to extract {filename}: {e}")

    if not text.strip():
        return (0, f"No text extracted from {filename}")

    chunks = _chunk_text(text)
    base_id = hashlib.md5(filename.encode("utf-8")).hexdigest()[:10]
    items = []
    for idx, chunk in enumerate(chunks):
        items.append({
            "id": f"upload::{base_id}::{idx}",
            "text": chunk,
            "metadata": {
                "source": "upload",
                "label": filename,
                "chunk_index": idx,
            },
        })
    added = store.add_many(items)
    return (added, None)


# ─── 3. JIRA ───────────────────────────────────────────────────────────────

def ingest_jira(max_results: Optional[int] = None) -> Tuple[int, int, Optional[str]]:
    """Pull past stories from Jira and index them.

    Returns (count_added, count_fetched, error_or_None) so the caller can tell
    whether a 0 means 'Jira returned nothing' (fetched=0 → auth/permission) vs
    'all already indexed' (fetched>0, added=0 → dedupe).
    """
    try:
        from rag.jira_importer import fetch_stories
        stories = fetch_stories(max_results=max_results)
    except Exception as e:
        return (0, 0, str(e))

    fetched = len(stories)
    items = []
    for s in stories:
        normalised = (s.get("normalised_text") or "").strip()
        if not normalised:
            continue
        items.append({
            "id": f"jira::{s.get('key')}",
            "text": normalised,
            "metadata": {
                "source": "jira",
                "label": s.get("key", ""),
                "summary": s.get("summary", ""),
            },
        })
    added = store.add_many(items)
    return (added, fetched, None)
