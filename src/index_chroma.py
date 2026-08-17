"""
Medical RAG - Index embedded chunks into Chroma
-----------------------------------------------
Input:  embedded_chunks.json (output of embed_guideline.py)
Output: a persistent Chroma HNSW collection ready for retrieval

Since embeddings come from a local PubMedBERT sentence-transformers model, the
collection is created with embedding_function=None and precomputed vectors are
supplied explicitly. Space is cosine (matches normalize_embeddings=True at
encode time, so distance = 1 - cosine similarity).

Recommendation grades (A/B/C/D/I) found in chunk text are extracted into
metadata so retrieval output can cite them directly.

Usage:
    python index_chroma.py [--chunks path] [--db path]
                           [--collection name] [--doc-id slug]
"""

import argparse
import json
from pathlib import Path

import chromadb

from grade import extract_grade


def main():
    parser = argparse.ArgumentParser(
        description="Index embedded_chunks.json into a persistent Chroma collection."
    )
    default_chunks = Path(__file__).resolve().parent / "data" / "embedded_chunks.json"
    parser.add_argument("--chunks", default=str(default_chunks))
    parser.add_argument("--db", default=str(default_chunks.parent / "chroma"))
    parser.add_argument("--collection", default="guidelines")
    parser.add_argument("--doc-id", default=None, help="slug identifying this doc (default: chunks file stem)")
    args = parser.parse_args()

    with open(args.chunks, encoding="utf-8") as f:
        chunks = json.load(f)
    doc_id = args.doc_id or Path(args.chunks).stem
    dim = len(chunks[0]["embedding"])

    client = chromadb.PersistentClient(path=args.db)
    collection = client.get_or_create_collection(
        name=args.collection,
        embedding_function=None,
        metadata={
            "embedding_model": "NeuML/pubmedbert-base-embeddings",
            "dimension": dim,
        },
        configuration={"hnsw": {"space": "cosine"}},
    )

    ids, documents, embeddings, metadatas = [], [], [], []
    for i, c in enumerate(chunks):
        meta = {
            "doc_id": doc_id,
            "chunk_index": i,
            "type": c.get("type"),
            "heading": c.get("heading"),
        }
        for k in ("org", "doc_title", "source_url"):
            if c.get(k):
                meta[k] = c[k]
        grade = extract_grade(c.get("text", ""))
        if grade:
            meta["grade"] = grade

        ids.append(f"{doc_id}-{i:04d}")
        documents.append(c["text"])
        embeddings.append(c["embedding"])
        metadatas.append(meta)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print(f"Indexed {len(ids)} chunks into '{args.collection}' (doc_id={doc_id})")
    print(f"Collection count: {collection.count()}")


if __name__ == "__main__":
    main()