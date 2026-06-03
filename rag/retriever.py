"""Build prompt-ready context blocks from retrieved similar documents.

A distance threshold filters out weak matches so only genuinely similar
past stories influence the prompt. ChromaDB cosine distance ranges 0..2
(0 = identical, ~1 = unrelated). Default keeps matches with distance
below MAX_DISTANCE.
"""

from typing import List, Dict

from rag.store import query

# Cosine distance cutoff. Matches with a LARGER distance than this are
# considered too weak to use as style reference and are dropped.
#   ~0.0–0.5  → strong match (same topic)
#   ~0.5–0.7  → moderate match (related)
#   ~0.7–1.0+ → weak / unrelated
MAX_DISTANCE = 0.65


def retrieve(notes: str, k: int = 3, max_distance: float = MAX_DISTANCE) -> List[Dict]:
    """Return raw top-k matches that pass the distance threshold (for UI display)."""
    matches = query(notes, k=k)
    return [m for m in matches if _passes(m, max_distance)]


def retrieve_all(notes: str, k: int = 3) -> List[Dict]:
    """Return ALL top-k matches without threshold filtering (for transparency/preview)."""
    return query(notes, k=k)


def _passes(match: Dict, max_distance: float) -> bool:
    dist = match.get("distance")
    if dist is None:
        return True  # no score → don't discard
    return dist <= max_distance


def retrieve_context(notes: str, k: int = 3, max_distance: float = MAX_DISTANCE) -> str:
    """Return formatted context block to inject into the story prompt.

    Only matches at-or-below `max_distance` are included. Empty string if
    nothing qualifies — the prompt then behaves as if RAG was off.
    """
    matches = retrieve(notes, k=k, max_distance=max_distance)
    if not matches:
        return ""

    blocks = []
    for i, m in enumerate(matches, start=1):
        src = (m.get("metadata") or {}).get("source", "unknown")
        label = (m.get("metadata") or {}).get("label", "")
        header = f"[Example {i} — source: {src}{(' · ' + label) if label else ''}]"
        # Truncate any one example to keep total prompt under control
        text = (m.get("text") or "").strip()
        if len(text) > 1500:
            text = text[:1500] + "...(truncated)"
        blocks.append(f"{header}\n{text}")

    return "\n\n".join(blocks)
