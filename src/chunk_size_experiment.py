"""
Medical RAG - Chunk-size / overlap sweep experiment
---------------------------------------------------
For each (max_tokens, overlap_tokens) config, re-chunk the source guideline,
embed with the local sentence-transformers model, run the same hybrid retrieval
(BM25 + vector, RRF) as production, and score Precision@5 using the ground-truth
relevance judgements in eval_questions.json.

Relevance rule (same spirit as evaluate_accuracy.py): a retrieved chunk counts
as relevant when its heading is one of the question's expected_sections OR its
text contains any of the question's answer_terms.

Does NOT touch the production index (src/data/chroma) - everything runs in
memory, so the existing 37-chunk collection is left alone.

Usage:
    python chunk_size_experiment.py [--sizes 200,400,600]
                                    [--overlaps 0,50,100]
                                    [--k 5]
"""
import argparse
import json
from itertools import product
from pathlib import Path

import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

from embed_guideline import load_and_chunk

SRC = Path(__file__).resolve().parent / "data" / "healthy-diet-phys-activity-high-risk-final-rec.json"
QS = Path(__file__).resolve().parent / "data" / "eval_questions.json"
MODEL = "NeuML/pubmedbert-base-embeddings"
RRF_K = 60
TOKEN_RE = __import__("re").compile(r"[a-z0-9]+")


def tokenize(t: str) -> list[str]:
    return TOKEN_RE.findall((t or "").lower())


def run_sweep(sizes, overlaps, k, model):
    with open(QS, encoding="utf-8") as f:
        questions = [q for q in json.load(f)["questions"] if not q.get("expected_out_of_scope", False)]

    print(f"{'size':>6} {'overlap':>8} {'chunks':>7} {'P@5':>6}  {'relev':>6}")
    rows = []
    for size, overlap in product(sizes, overlaps):
        chunks = load_and_chunk(str(SRC), max_tokens=size, overlap_tokens=overlap)
        texts = [c["text"] for c in chunks]
        vecs = model.encode(texts, normalize_embeddings=True)
        bm25 = BM25Okapi([tokenize(t) for t in texts])

        per_q = []
        for q in questions:
            qv = model.encode([q["query"]], normalize_embeddings=True)[0]
            sims = vecs @ qv
            vrank = np.argsort(-sims)
            bm_scores = bm25.get_scores(tokenize(q["query"]))
            bm_rank = np.argsort(-bm_scores)

            fused = {}
            for r, cid in enumerate(vrank.tolist()):
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + r + 1)
            for r, cid in enumerate(bm_rank.tolist()):
                if bm_scores[cid] > 0:
                    fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + r + 1)

            top = [cid for cid, _ in sorted(fused.items(), key=lambda x: x[1], reverse=True)][:k]

            expected = [s.lower() for s in q.get("expected_sections", [])]
            terms = [t.lower() for t in q.get("answer_terms", [])]
            relevant = 0
            for cid in top:
                c = chunks[cid]
                heading = (c.get("heading") or "").lower()
                if heading in expected:
                    relevant += 1
                    continue
                if terms and any(t in c["text"].lower() for t in terms):
                    relevant += 1
            per_q.append(relevant / k)

        p5 = sum(per_q) / len(per_q)
        rows.append((size, overlap, len(chunks), p5))
        print(f"{size:>6} {overlap:>8} {len(chunks):>7} {p5:>6.3f}  {p5*5:>6.2f}")

    return rows


def main():
    parser = argparse.ArgumentParser(description="Chunk-size/overlap P@5 sweep.")
    parser.add_argument("--sizes", default="200,400,600")
    parser.add_argument("--overlaps", default="0,50,100")
    parser.add_argument("--k", type=int, default=5)
    args = parser.parse_args()
    sizes = [int(x) for x in args.sizes.split(",")]
    overlaps = [int(x) for x in args.overlaps.split(",")]
    model = SentenceTransformer(MODEL)
    run_sweep(sizes, overlaps, args.k, model)


if __name__ == "__main__":
    main()
