"""
Medical RAG - interactive CLI over the shared query pipeline
-------------------------------------------------------------
Embeds the question with the same local PubMedBERT model used at index time and
runs the production pipeline (controllers/query.py): hybrid retrieval, confidence
gating, LLM answer generation, and per-answer quality scoring.

Out-of-source questions are flagged with a disclaimer instead of a made-up
answer; the overall model accuracy from the latest evaluation is printed after
the hits.

Usage:
    rag/bin/python -m tools.query_chroma "question..." [--k 5]
                                       [--strategy hybrid|vector] [--no-llm]
"""

import argparse

from modules.pipeline import answer_query, accuracy_summary


def main():
    parser = argparse.ArgumentParser(description="Search guideline chunks in Chroma.")
    parser.add_argument("query")
    parser.add_argument("--k", type=int, default=5, help="number of hits (default 5)")
    parser.add_argument(
        "--strategy",
        choices=["hybrid", "vector"],
        default="hybrid",
        help="retrieval strategy (default hybrid = BM25 + vector)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.30,
        help="below this top similarity (0-1), show the disclaimer (default 0.30)",
    )
    parser.add_argument(
        "--no-grade-gate",
        action="store_true",
        help="disable the grade-based disclaimer for decision-style questions",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="skip LLM answer generation and print only the retrieved hits",
    )
    args = parser.parse_args()

    result = answer_query(
        args.query,
        k=args.k,
        strategy=args.strategy,
        use_llm=not args.no_llm,
        sim_threshold=args.threshold,
        use_grade_gate=not args.no_grade_gate,
    )

    print(f"Top {len(result['hits'])} hits for: {args.query}  (strategy: {args.strategy})\n")

    if result["disclaimed"]:
        print(result["message"])
        print()
    elif not args.no_llm and not result["message"].startswith("(LLM answer unavailable"):
        print(f"ANSWER: {result['message']}\n")
        print("Sources consulted:\n")

    for hit in result["hits"]:
        grade = hit["grade"] or "n/a"
        print(f"[Hit {hit['rank']}] similarity={hit['similarity']:.3f} | Grade {grade} | {hit['org']}")
        if hit["section"]:
            print(f"  section: {hit['section']}")
        print(f"  text: {hit['text'][:400]}")
        print()

    if result["quality"]:
        print(
            f"quality: faithfulness={result['quality']['faithfulness']} "
            f"citation_accuracy={result['quality']['citation_accuracy']}"
        )
        print()

    acc = accuracy_summary()
    if acc:
        print(acc)
    else:
        print(
            "Model accuracy not found -- run: "
            "rag/bin/python -m tools.evaluate_accuracy"
        )


if __name__ == "__main__":
    main()