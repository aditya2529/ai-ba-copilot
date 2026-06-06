"""Embedding backend with automatic light/full fallback.

Both backends use the SAME model — all-MiniLM-L6-v2 (384-dim) — so vectors are
interchangeable. The backend is chosen automatically at runtime:

  • FULL  — `sentence-transformers` (PyTorch). Best on a dev machine where torch
            is already installed. Heavier (~1GB with torch).
  • LIGHT — ChromaDB's built-in ONNX MiniLM embedder (onnxruntime, ~80MB, no
            torch). Used automatically when sentence-transformers isn't
            installed — ideal for Streamlit Cloud's 1GB memory limit.

Local machine: keep sentence-transformers installed → FULL backend.
Cloud: omit sentence-transformers from requirements → LIGHT backend.
The embeddings are equivalent either way.
"""

from typing import List

_backend = None  # tuple: (kind, callable-or-model)
_DIM = 384


def _get_backend():
    """Resolve the embedding backend once, preferring the full (torch) one."""
    global _backend
    if _backend is None:
        try:
            # FULL backend — sentence-transformers (PyTorch)
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            _backend = ("st", model)
        except Exception:
            # LIGHT backend — ChromaDB's ONNX MiniLM (no torch)
            from chromadb.utils import embedding_functions
            ef = embedding_functions.ONNXMiniLM_L6_V2()
            _backend = ("onnx", ef)
    return _backend


def backend_name() -> str:
    """Return which backend is active: 'sentence-transformers' or 'onnx'."""
    kind, _ = _get_backend()
    return "sentence-transformers" if kind == "st" else "onnx"


def embed(text: str) -> List[float]:
    """Convert a single string into a 384-dim vector of plain Python floats."""
    if not text or not text.strip():
        return [0.0] * _DIM
    kind, m = _get_backend()
    if kind == "st":
        return m.encode(text, normalize_embeddings=True).tolist()
    # ONNX embedding function takes a list, returns a list of vectors.
    # Force plain Python floats — ChromaDB rejects numpy float32 on add().
    return [float(x) for x in m([text])[0]]


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Convert many strings into vectors of plain Python floats in one pass."""
    if not texts:
        return []
    kind, m = _get_backend()
    if kind == "st":
        return m.encode(texts, normalize_embeddings=True).tolist()
    return [[float(x) for x in v] for v in m(texts)]
