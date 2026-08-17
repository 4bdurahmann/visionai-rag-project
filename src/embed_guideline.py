"""
Medical RAG - Chunking + Embedding step
----------------------------------------
Input:  LlamaParse-style JSON (the structured output you parsed a guideline PDF into)
Output: a list of chunks, each with its embedding vector, ready for a vector store

Model: NeuML/pubmedbert-base-embeddings (sentence-transformers compatible)
  - Domain-tuned on biomedical text (PubMedBERT backbone), not general web text.
  - Runs 100% locally, no API calls, no per-token cost.
  - 768-dim, mean pooling, max_seq_length 512 (long chunks are truncated).

Chunking: heading-bounded sections; tables isolated with a caption (from a
  preceding "Table N." / "Figure." line when the parser emits it as text,
  otherwise from the nearest heading); header/footer/link items dropped.

Usage:
    python embed_guideline.py [JSON_PATH] [-o OUT] [--org ORG]
                              [--doc-title TITLE] [--source-url URL]

Install first:
    pip install sentence-transformers

NOTE: the model download (~440MB) happens on first run and requires internet
access to huggingface.co.
"""

import argparse
import json
import re
from pathlib import Path

from sentence_transformers import SentenceTransformer

_TABLE_TITLE_RE = re.compile(r"^(Table|Figure)(\s+\d+)?[.:]")


def _split_table_rows(caption: str, rows, md: str) -> list[str]:
    """
    Split a table into one chunk per row so individual facts (a Q&A row, a
    rationale label) embed on their own instead of being diluted inside one
    giant table chunk. Rows with an empty first cell (headers) are skipped.
    Falls back to the whole markdown table when there are no usable rows.
    """
    if not rows:
        return [caption + "\n" + md]
    parts = []
    for row in rows:
        label = (row[0] or "").strip()
        if not label:
            continue
        cells = [c.strip() for c in row[1:] if c and c.strip()]
        if len(row) == 2 and cells:
            parts.append(f"{label}: {cells[0]}")
        elif cells:
            parts.append(label + "\n" + "\n".join(f"- {c}" for c in cells))
    if not parts:
        return [caption + "\n" + md]
    return [f"{caption}\n{part}" for part in parts]


def load_and_chunk(json_path: str, doc_meta: dict | None = None) -> list[dict]:
    """
    Turn LlamaParse-style page/item JSON into heading-bounded chunks,
    keeping tables isolated with a short caption so they embed meaningfully
    on their own instead of being merged into surrounding prose.

    doc_meta (e.g. {"org": "USPSTF", "doc_title": ..., "source_url": ...})
    is stamped onto every chunk so the vector-store artifact keeps its
    provenance for citation at retrieval time.
    """
    doc_meta = doc_meta or {}
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    pages = data["pages"]
    chunks = []
    current_heading = None
    current_buffer = []
    pending_caption = None

    def flush():
        if current_buffer:
            text = "\n".join(current_buffer).strip()
            if text:
                chunks.append(
                    {
                        "type": "section",
                        "heading": current_heading,
                        "text": text,
                        **doc_meta,
                    }
                )

    for p in pages:
        for it in p["items"]:
            t = it["type"]
            if t == "heading":
                flush()
                current_buffer.clear()
                current_heading = it["value"]
                # use the parser's markdown line to preserve heading level markers
                current_buffer.append(it.get("md") or f"# {current_heading}")
                pending_caption = None
            elif t in ("text", "list"):
                value = it.get("value") or it.get("md", "")
                current_buffer.append(value)
                # LlamaParse sometimes emits a "Table 2." title as plain text;
                # remember it so the next table chunk gets the right caption.
                if t == "text" and _TABLE_TITLE_RE.match(value.strip()):
                    pending_caption = value.strip()
            elif t == "table":
                # the caption line is already in the prose buffer; drop the dup
                if pending_caption and current_buffer and current_buffer[-1].strip() == pending_caption:
                    current_buffer.pop()
                flush()
                current_buffer.clear()
                caption = (
                    pending_caption
                    or (
                        f"Table from section '{current_heading}'"
                        if current_heading
                        else "Table"
                    )
                )
                heading = pending_caption or current_heading
                pending_caption = None
                for row_text in _split_table_rows(caption, it.get("rows"), it.get("md", "")):
                    chunks.append(
                        {
                            "type": "table",
                            "heading": heading,
                            "text": row_text,
                            **doc_meta,
                        }
                    )
            # header / footer / link items are skipped as boilerplate noise
    flush()

    # drop junk: masthead lines before the first heading (heading is None)
    # and tiny fragments (e.g. a lone abbreviation line)
    chunks = [
        c
        for c in chunks
        if not (c["type"] == "section" and c["heading"] is None)
        and len(c["text"]) > 40
    ]
    return chunks


def embed_chunks(
    chunks: list[dict], model_name: str = "NeuML/pubmedbert-base-embeddings"
):
    """
    Encode each chunk's text into a dense vector using a biomedical-domain model.
    """
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    vectors = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,  # cosine similarity becomes a simple dot product
    )
    for c, v in zip(chunks, vectors):
        c["embedding"] = v.tolist()
    return chunks


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Chunk + embed a LlamaParse guideline JSON for a vector store."
    )
    default_json = (
        Path(__file__).resolve().parent
        / "data"
        / "healthy-diet-phys-activity-high-risk-final-rec.json"
    )
    parser.add_argument("json_path", nargs="?", default=str(default_json))
    default_output = str(Path(default_json).parent / "embedded_chunks.json")
    parser.add_argument("-o", "--output", default=default_output)
    parser.add_argument("--org", default="USPSTF")
    parser.add_argument("--doc-title", default="")
    parser.add_argument("--source-url", default="")
    args = parser.parse_args()

    meta = {
        k: v
        for k, v in {
            "org": args.org,
            "doc_title": args.doc_title,
            "source_url": args.source_url,
        }.items()
        if v
    }

    chunks = load_and_chunk(args.json_path, doc_meta=meta)
    print(f"Built {len(chunks)} chunks")

    chunks = embed_chunks(chunks)
    print(f"Embedded {len(chunks)} chunks, vector dim = {len(chunks[0]['embedding'])}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(chunks, f)
    print(f"Saved to {args.output}")