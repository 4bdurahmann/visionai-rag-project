"""
Heavy application state: embedding model, Chroma client, and the hybrid
retriever, loaded exactly once per process behind a cache.

Importing this module is cheap; the expensive objects are only created on the
first call to :func:`get_engine`, so CLI tools that do not need inference
(e.g. ``chunk_size_experiment``, which builds its own in-memory index) stay
light, and the API does not pay the model-load cost at import time.
"""

from types import SimpleNamespace

import chromadb
from sentence_transformers import SentenceTransformer

from modules import config
from controllers.retrieval import HybridRetriever


def get_engine() -> SimpleNamespace:
    """Lazily build and cache the shared runtime objects.

    Returns:
        SimpleNamespace with ``model``, ``client``, ``collection`` and
        ``retriever`` attributes.
    """
    if get_engine.cache is None:
        model = SentenceTransformer(config.MODEL_NAME)
        client = chromadb.PersistentClient(path=config.DEFAULT_DB)
        collection = client.get_or_create_collection(
            name=config.COLLECTION, embedding_function=None
        )
        retriever = HybridRetriever(collection, strategy="hybrid")
        get_engine.cache = SimpleNamespace(
            model=model,
            client=client,
            collection=collection,
            retriever=retriever,
        )
    return get_engine.cache


get_engine.cache = None  # type: ignore[attr-defined]