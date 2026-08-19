"""
Medical RAG - Shared retrieval backends (vector-only and hybrid BM25+vector)
---------------------------------------------------------------------------
Both strategies query a Chroma collection. In hybrid mode, BM25 candidates are
used as a recall extension and hits are ranked by an RRF-fused score, so exact
numbers/names that a pure semantic ranking would bury still surface.

Embedding space is cosine with normalized vectors (see index_chroma.py), so
vector similarity = 1 - distance.
"""

import re

from rank_bm25 import BM25Okapi

TOKEN_RE = re.compile(r"[a-z0-9]+")
RRF_K = 60  # standard RRF constant


def _tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall((text or "").lower())


def _cosine_sim(distance: float) -> float:
    return 1.0 - distance


def load_corpus(collection) -> dict:
    """Pull every stored record (id, text, metadata) from the collection."""
    got = collection.get(include=["documents", "metadatas"])
    corpus = {}
    for cid, doc, meta in zip(got["ids"], got["documents"], got["metadatas"]):
        corpus[cid] = {"text": doc, "meta": meta}
    return corpus


class HybridRetriever:
    def __init__(self, collection, strategy: str = "hybrid"):
        """
        strategy: "hybrid" (BM25 recall + vector similarity ranking) or "vector".
        """
        self.collection = collection
        self.strategy = strategy
        self.corpus = load_corpus(collection) if strategy == "hybrid" else None
        self.bm25 = None
        if self.corpus:
            tokenized = [_tokenize(d["text"]) for d in self.corpus.values()]
            self.bm25 = BM25Okapi(tokenized)

    @property
    def cids(self) -> list[str]:
        return list(self.corpus) if self.corpus else []

    def search(self, query_text: str, query_vector, k: int, depth: int = 40):
        """
        Return up to k results as list of (cid, sim, fused, doc, meta).
        sim   - cosine similarity from the vector ranking (reported for reference)
        fused - RRF score over vector + BM25 ranks; the ordering key in hybrid
                mode (equals sim in vector mode).
        Ranking order is the strategy's order.
        """
        depth = max(depth, k)

        vector_ranks = {}
        vector_sims = {}
        vres = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=depth,
            include=["documents", "metadatas", "distances"],
        )
        for cid, dist in zip(vres["ids"][0], vres["distances"][0]):
            vector_ranks[cid] = len(vector_ranks)
            vector_sims[cid] = _cosine_sim(dist)

        if self.strategy != "hybrid" or not self.bm25:
            hits = []
            for cid, doc, meta, dist in zip(
                vres["ids"][0], vres["documents"][0],
                vres["metadatas"][0], vres["distances"][0],
            ):
                sim = _cosine_sim(dist)
                hits.append((cid, sim, sim, doc, meta))
            return hits[:k]

        scores = self.bm25.get_scores(_tokenize(query_text))
        bm25_ranks = [cid for cid, s in sorted(zip(self.cids, scores), key=lambda x: x[1], reverse=True) if s > 0]

        fused = {}
        for rank, cid in enumerate(vector_ranks):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + rank + 1)
        for rank, cid in enumerate(bm25_ranks):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + rank + 1)

        # rank by the RRF-fused score: vector similarity catches semantic
        # matches while BM25 promotes exact-number/name evidence chunks that a
        # pure semantic ranking can bury (e.g. "pooled RR, 0.81").
        ordered = [cid for cid, _ in sorted(fused.items(), key=lambda x: x[1], reverse=True)]
        return self._to_hits(ordered[:k], vector_sims, fused)

    def _to_hits(self, ordered: list[str], vector_sims: dict, fused: dict):
        hits = []
        for cid in ordered:
            if cid not in self.corpus:
                continue
            d = self.corpus[cid]
            hits.append((cid, vector_sims.get(cid, 0.0), fused.get(cid, 0.0), d["text"], d["meta"]))
        return hits