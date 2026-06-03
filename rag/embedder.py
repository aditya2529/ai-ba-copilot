"""Local sentence-transformers embedder.

Uses `all-MiniLM-L6-v2` — small (~80MB), fast, CPU-friendly, no API key
required. The model is lazily loaded on first call so app cold-start
remains fast for users who never visit the RAG page.
"""

from typing import List

_model = None
_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def _get_model():
    """Load the model on first use; cache for subsequent calls."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed(text: str) -> List[float]:
    """Convert a single string into a vector."""
    if not text or not text.strip():
        # Return a zero vector matching model dimension (384 for MiniLM-L6).
        return [0.0] * 384
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Convert many strings into vectors in one pass (faster than looping)."""
    if not texts:
        return []
    model = _get_model()
    vectors = model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()
