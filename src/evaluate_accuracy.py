"""
Medical RAG - Answer accuracy evaluation
----------------------------------------
Runs the same retrieval + disclaimer gates used by query_chroma.py against a
set of ground-truth questions written from the guideline PDF itself, then
judges each answer as correct / incorrect and writes the full breakdown to a
JSON file so each response can be inspected.

Correctness rules (per question, using its "expected_out_of_scope" flag):
  - out-of-scope question -> correct iff the disclaimer was shown
  - in-scope question     -> correct iff the disclaimer was NOT shown AND the
                             expected_sections include the heading of at least
                             one retrieved chunk AND every ground-truth phrase
                             (answer_terms) appears in the retrieved chunk text

The answer window is top-3 by default (top-1 is too strict, top-5 too lenient
on a 22-chunk corpus); pass --k to change it.

--judge llm replaces the keyword/section checks for in-scope questions with a
Groq LLM verdict (GROQ_API_KEY required); out-of-scope questions are still
judged by whether the disclaimer fired.

Output:
  src/data/accuracy_results.json  - overall accuracy + per-question detail

Usage:
    python evaluate_accuracy.py [--k 3] [--strategy hybrid|vector]
                                [--questions path] [--json-out path]
                                [--judge heuristic|llm]
"""

import argparse
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from retrieval import HybridRetriever
from gate import disclaim, GRADE_LOOKAHEAD
from llm import judge_answer

DEFAULT_DB = str(Path(__file__).resolve().parent / "data" / "chroma")
DEFAULT_MODEL = "NeuML/pubmedbert-base-embeddings"
DEFAULT_QUESTIONS = str(Path(__file__).resolve().parent / "data" / "eval_questions.json")
DEFAULT_OUT = str(Path(__file__).resolve().parent / "data" / "accuracy_results.json")


def judge(query, hits, disclaim_msg, q) -> tuple[bool, str]:
    expected_oos = q.get("expected_out_of_scope", False)
    disclaimed = bool(disclaim_msg)

    if expected_oos:
        return (disclaimed, "disclaimed" if disclaimed else "NOT disclaimed (should have)")
    if disclaimed:
        return (False, "in-scope question was disclaimed")

    expected_sections = [s.lower() for s in q.get("expected_sections", [])]
    if expected_sections:
        found = [meta.get("heading") for _, _, _, _, meta in hits if meta.get("heading")]
        if not any(h.lower() in expected_sections for h in found):
            return (
                False,
                f"none of the top-{len(hits)} hits is from an expected section; "
                f"got: {found[:3]}",
            )

    terms = [t.lower() for t in q.get("answer_terms", [])]
    retrieved = " ".join(doc for _, _, _, doc, _ in hits).lower()
    missing = [t for t in terms if t not in retrieved]
    if missing:
        return (False, f"missing terms in retrieved text: {missing}")
    return (True, "an expected section is retrieved and all terms found")


def main():
    parser = argparse.ArgumentParser(description="Evaluate answer accuracy against ground truth.")
    parser.add_argument("--k", type=int, default=3,
                        help="number of retrieved chunks used to judge each answer "
                             "(default 3 - the answer window; top-1 is too strict, top-5 too lenient on a 22-chunk corpus)")
    parser.add_argument("--strategy", choices=["hybrid", "vector"], default="hybrid")
    parser.add_argument("--db", default=DEFAULT_DB)
    parser.add_argument("--collection", default="guidelines")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--questions", default=DEFAULT_QUESTIONS)
    parser.add_argument("--json-out", default=DEFAULT_OUT)
    parser.add_argument("--judge", choices=["heuristic", "llm"], default="heuristic",
                        help="how in-scope answers are judged (default heuristic; "
                             "llm uses Groq, GROQ_API_KEY required)")
    args = parser.parse_args()

    with open(args.questions, encoding="utf-8") as f:
        questions = json.load(f)["questions"]

    model = SentenceTransformer(args.model)
    client = chromadb.PersistentClient(path=args.db)
    collection = client.get_collection(args.collection)
    retriever = HybridRetriever(collection, strategy=args.strategy)

    results = []
    for q in questions:
        qv = model.encode([q["query"]], normalize_embeddings=True)[0]
        # grade gate looks further down the ranking than the k shown to the user
        hits = retriever.search(q["query"], qv, max(args.k, GRADE_LOOKAHEAD))
        msg, _reason = disclaim(q["query"], hits)
        hits_full = hits
        hits = hits[: args.k]
        if args.judge == "llm" and not q.get("expected_out_of_scope", False):
            # judge with the same full context the answer generator is given
            llm_ok, llm_reason = judge_answer(q["query"], hits_full, q.get("expected_answer", ""))
            if llm_ok is not None:
                correct, reason = llm_ok, f"llm judge: {llm_reason}"
            else:
                correct, reason = judge(q["query"], hits, msg, q)
                reason = f"fallback: {reason} ({llm_reason})"
        else:
            correct, reason = judge(q["query"], hits, msg, q)
        results.append(
            {
                "id": q["id"],
                "category": q.get("category"),
                "query": q["query"],
                "expected_answer": q.get("expected_answer"),
                "expected_out_of_scope": q.get("expected_out_of_scope", False),
                "disclaimed": bool(msg),
                "top_sections": [meta.get("heading") for _, _, _, _, meta in hits],
                "top_similarity": round(max(sim for _, sim, _, _, _ in hits), 3) if hits else None,
                "retrieved_text": " ".join(doc for _, _, _, doc, _ in hits),
                "correct": correct,
                "reason": reason,
            }
        )

    n = len(results)
    correct = sum(r["correct"] for r in results)
    by_category: dict[str, list] = {}
    for r in results:
        by_category.setdefault(r["category"], []).append(r)

    report = {
        "model": args.model,
        "strategy": args.strategy,
        "judge": args.judge,
        "collection": args.collection,
        "top_k": args.k,
        "n_questions": n,
        "n_correct": correct,
        "accuracy": round(correct / n, 4) if n else None,
        "category_accuracy": {
            cat: {"n": len(rs), "correct": sum(r["correct"] for r in rs)}
            for cat, rs in by_category.items()
        },
        "results": results,
    }

    with open(args.json_out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Answer accuracy ({args.strategy}, top-{args.k}): {correct}/{n} = {correct / n * 100:.1f}%")
    for cat, rs in sorted(by_category.items()):
        ok = sum(r["correct"] for r in rs)
        print(f"  {cat:<14} {ok}/{len(rs)}")
    print(f"Per-question detail written to: {args.json_out}")


if __name__ == "__main__":
    main()
