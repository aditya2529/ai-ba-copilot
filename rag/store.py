"""ChromaDB persistent vector store wrapper.

Persists to `./chroma_db/` next to the app — file-based, no server,
no cloud account. All entries are tagged with a `source` in metadata
("history" / "upload" / "jira") so retrieval can show provenance.
"""

import os
from typing import List, Dict, Optional

from rag.embedder import embed, embed_batch

_CHROMA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
_COLLECTION_NAME = "ba_corpus"

_client = None
_collection = None


def _get_collection():
    """Lazy-load Chroma client + collection. Persists to disk."""
    global _client, _collection
    if _collection is None:
        import chromadb
        from chromadb.config import Settings
        _client = chromadb.PersistentClient(
            path=_CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
        _collection = _client.get_or_create_collection(
            name=_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def exists(doc_id: str) -> bool:
    """Check whether a document with this id is already indexed (dedupe)."""
    col = _get_collection()
    try:
        result = col.get(ids=[doc_id])
        return bool(result and result.get("ids"))
    except Exception:
        return False


def add(doc_id: str, text: str, metadata: Optional[Dict] = None) -> bool:
    """Add a single document. Returns True if added, False if skipped (already exists or empty)."""
    if not text or not text.strip():
        return False
    if exists(doc_id):
        return False
    col = _get_collection()
    vector = embed(text)
    col.add(
        ids=[doc_id],
        embeddings=[vector],
        documents=[text],
        metadatas=[metadata or {}],
    )
    return True


def add_many(items: List[Dict]) -> int:
    """Bulk add. Each item: {id, text, metadata}. Skips duplicates and empty text. Returns count added."""
    if not items:
        return 0
    fresh = []
    for it in items:
        if not it.get("text") or not it["text"].strip():
            continue
        if exists(it["id"]):
            continue
        fresh.append(it)
    if not fresh:
        return 0
    col = _get_collection()
    texts = [it["text"] for it in fresh]
    vectors = embed_batch(texts)
    col.add(
        ids=[it["id"] for it in fresh],
        embeddings=vectors,
        documents=texts,
        metadatas=[it.get("metadata") or {} for it in fresh],
    )
    return len(fresh)


def query(text: str, k: int = 3) -> List[Dict]:
    """Return top-k similar documents. Each result: {id, text, metadata, distance}."""
    if not text or not text.strip():
        return []
    col = _get_collection()
    if col.count() == 0:
        return []
    vector = embed(text)
    result = col.query(query_embeddings=[vector], n_results=min(k, col.count()))
    out = []
    ids = (result.get("ids") or [[]])[0]
    docs = (result.get("documents") or [[]])[0]
    metas = (result.get("metadatas") or [[]])[0]
    dists = (result.get("distances") or [[]])[0]
    for i in range(len(ids)):
        out.append({
            "id": ids[i],
            "text": docs[i] if i < len(docs) else "",
            "metadata": metas[i] if i < len(metas) else {},
            "distance": dists[i] if i < len(dists) else None,
        })
    return out


def count() -> Dict[str, int]:
    """Return total count plus breakdown by source."""
    col = _get_collection()
    total = col.count()
    breakdown = {"total": total, "history": 0, "upload": 0, "jira": 0}
    if total == 0:
        return breakdown
    # Iterate metadata to count by source
    try:
        all_items = col.get()
        for meta in all_items.get("metadatas", []) or []:
            src = (meta or {}).get("source", "other")
            if src in breakdown:
                breakdown[src] += 1
    except Exception:
        pass
    return breakdown


def reset():
    """Delete the entire collection. Used by 'rebuild from scratch' flows."""
    global _client, _collection
    col = _get_collection()
    try:
        _client.delete_collection(_COLLECTION_NAME)
    except Exception:
        pass
    _collection = None  # force re-create on next access
