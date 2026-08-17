"""
Medical RAG - Query a Chroma collection of embedded guideline chunks
--------------------------------------------------------------------
Embeds the question with the same local PubMedBERT model used at index time,
searches the collection (hybrid BM25+vector by default, or vector-only), and
prints each hit citing recommendation grade + source organization + source
document. Out-of-source questions are flagged with a disclaimer instead of a
made-up answer, and the overall model accuracy is printed at the end.

By default the top hits are turned into a natural-language answer by a Groq
LLM (GROQ_API_KEY); pass --no-llm to print only the raw hits.

Usage:
    python query_chroma.py "question..." [--k 5] [--strategy hybrid|vector]
                           [--db path] [--collection name] [--model name]
                           [--no-llm]
"""

import argparse
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from retrieval import HybridRetriever
from grade import extract_grade
from gate import disclaim, GRADE_LOOKAHEAD, DEFAULT_SIM_THRESHOLD
from llm import generate_answer

DEFAULT_DB = str(Path(__file__).resolve().parent / "data" / "chroma")
MODEL_NAME = "NeuML/pubmedbert-base-embeddings"
ACCURACY_PATH = str(Path(__file__).resolve().parent / "data" / "accuracy_results.json")


def _answer_from_hits(args, query_text, hits) -> str:
    try:
        return generate_answer(query_text, hits)
    except Exception as exc:  # noqa: BLE001 - fail gracefully back to raw hits
        return f"(LLM answer unavailable: {exc})"


def model_accuracy(accuracy_path: str = ACCURACY_PATH) -> str | None:
    """Overall model accuracy from the answer-evaluation report
    (src/evaluate_accuracy.py -> src/data/accuracy_results.json)."""
    try:
        with open(accuracy_path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

    n = data.get("n_questions")
    correct = data.get("n_correct")
    acc = data.get("accuracy")
    if not n or acc is None:
        return None

    lines = [
        f"Model accuracy: {correct}/{n} = {acc * 100:.1f}% "
        f"({data.get('strategy')}, top-{data.get('top_k')})"
    ]
    by_cat = data.get("category_accuracy") or {}
    for cat in sorted(by_cat):
        c = by_cat[cat]
        lines.append(f"  {cat:<15} {c['correct']}/{c['n']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search guideline chunks in Chroma.")
    parser.add_argument("query")
    parser.add_argument("--k", type=int, default=5, help="number of results (default 5)")
    parser.add_argument(
        "--strategy",
        choices=["hybrid", "vector"],
        default="hybrid",
        help="retrieval strategy (default hybrid = BM25 + vector)",
    )
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--collection", default="guidelines")
    parser.add_argument("--model", default=MODEL_NAME)
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_SIM_THRESHOLD,
        help=f"below this top similarity (0-1), show the disclaimer (default {DEFAULT_SIM_THRESHOLD})",
    )
    parser.add_argument(
        "--no-grade-gate",
        action="store_true",
        help="disable the grade-based disclaimer for decision-style questions",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="skip the Groq answer generation and print only the retrieved hits",
    )
    args = parser.parse_args()

    model = SentenceTransformer(args.model)
    qv = model.encode([args.query], normalize_embeddings=True)[0]

    client = chromadb.PersistentClient(path=args.db)
    collection = client.get_collection(args.collection)
    retriever = HybridRetriever(collection, strategy=args.strategy)

    # fetch a few extra hits than shown so the grade gate can look further down
    # the ranking for a graded recommendation chunk
    k_full = max(args.k, GRADE_LOOKAHEAD)
    hits = retriever.search(args.query, qv, k_full)
    msg, _reason = disclaim(
        args.query,
        hits,
        sim_threshold=args.threshold,
        use_grade_gate=not args.no_grade_gate,
    )
    hits_full = hits
    hits = hits[: args.k]

    print(f"Top {len(hits)} hits for: {args.query}  (strategy: {args.strategy})\n")

    if not msg and not args.no_llm:
        # generate the answer from the full retrieval context (the LLM picks the
        # relevant excerpts itself), then show the top-k sources
        answer = _answer_from_hits(args, args.query, hits_full)
        if not answer.startswith("(LLM answer unavailable"):
            print(f"ANSWER: {answer}\n")
            print("Sources consulted:\n")

    if msg:
        print(msg)
        print()

    for i, (_cid, sim, fused, doc, meta) in enumerate(hits, 1):
        grade = meta.get("grade") or extract_grade(doc)
        org = meta.get("org") or "?"
        heading = meta.get("heading") or ""
        title = meta.get("doc_title") or ""
        url = meta.get("source_url") or ""

        grade_str = f"Grade {grade}" if grade else "Grade n/a"
        print(f"[Hit {i}] similarity={sim:.3f} | fused={fused:.4f} | {grade_str} | {org}")
        if heading:
            print(f"  section: {heading}")
        if title or url:
            print(f"  source: {title} {url}".rstrip())
        print(f"  text: {doc[:400]}")
        print()

    acc = model_accuracy()
    if acc:
        print(acc)
    else:
        print(
            "Model accuracy not found -- run: "
            "rag/bin/python src/evaluate_accuracy.py"
        )


if __name__ == "__main__":
    main()