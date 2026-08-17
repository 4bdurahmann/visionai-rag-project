"""
Medical RAG - Groq LLM integration
----------------------------------
Two jobs:
  1. generate_answer  - turn the retrieved chunks into a natural-language answer
                        that cites section + recommendation grade + source org.
  2. judge_answer     - evaluate (in evaluate_accuracy.py) whether the retrieved
                        chunks are sufficient to answer a ground-truth question.

The API key is read from the GROQ_API_KEY environment variable (never hardcoded);
the model can be overridden with GROQ_MODEL. All calls go through the official
`groq` SDK, so no base-url/auth plumbing is needed.
"""

import os
import re

from groq import Groq

DEFAULT_MODEL = "openai/gpt-oss-20b"

_ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def _load_dotenv(path: str = _ENV_FILE) -> None:
    """Minimal .env loader: reads KEY=VALUE lines into os.environ (no override)."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())
    except OSError:
        pass


_load_dotenv()

_SYSTEM_ANSWER = (
    "You are a medical Q&A assistant over USPSTF/CDC/WHO clinical guideline "
    "documents. Answer the user's question using ONLY the provided source "
    "excerpts. Cite the section and, when present, the recommendation grade and "
    "the issuing organization. If the excerpts do not contain the answer, say "
    "so clearly instead of guessing. Be concise and factual."
)

_SYSTEM_JUDGE = (
    "You are evaluating a medical RAG retrieval system. You are given a "
    "question, the ground-truth expected answer, and the source excerpts the "
    "system retrieved. Reply on a single line starting with exactly 'CORRECT' "
    "or 'INCORRECT', followed by a short reason. Judge CORRECT only if the "
    "retrieved excerpts actually contain the information needed to answer the "
    "question; partial or off-topic excerpts are INCORRECT."
)


def get_client() -> Groq:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set - export it first, e.g. "
            "export GROQ_API_KEY=gsk_..."
        )
    return Groq(api_key=key)


def model_name() -> str:
    return os.environ.get("GROQ_MODEL", DEFAULT_MODEL)


def _excerpts(hits) -> str:
    lines = []
    for i, (_cid, _sim, _fused, doc, meta) in enumerate(hits, 1):
        heading = meta.get("heading") or "untitled section"
        org = meta.get("org") or "?"
        grade = meta.get("grade")
        grade_str = f", Grade {grade}" if grade else ""
        lines.append(f"[{i}] Section: {heading} ({org}{grade_str})\n{doc[:1500]}")
    return "\n\n".join(lines)


def _chat(client: Groq, system: str, user: str, temperature: float = 0.2) -> str:
    resp = client.chat.completions.create(
        model=model_name(),
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def generate_answer(query_text: str, hits) -> str:
    """Natural-language answer over the retrieved chunks (RAG generation)."""
    user = (
        f"Question: {query_text}\n\n"
        f"Source excerpts (top {len(hits)} retrieved chunks):\n{_excerpts(hits)}"
    )
    return _chat(get_client(), _SYSTEM_ANSWER, user)


def judge_answer(query_text: str, hits, expected_answer: str) -> tuple[bool | None, str]:
    """LLM judge: is the retrieved information sufficient to answer correctly?
    Returns (correct, reason); on any API/config error returns (None, error)."""
    try:
        user = (
            f"Question: {query_text}\n"
            f"Expected answer (ground truth): {expected_answer}\n\n"
            f"Retrieved source excerpts (top {len(hits)}):\n{_excerpts(hits)}\n\n"
            "Verdict (single line): CORRECT or INCORRECT"
        )
        out = _chat(get_client(), _SYSTEM_JUDGE, user)
    except Exception as exc:  # noqa: BLE001 - report any API error to the caller
        return None, f"llm error: {exc}"

    m = re.match(r"\b(CORRECT|INCORRECT)\b", out.upper())
    if not m:
        return None, f"unparseable LLM verdict: {out[:120]!r}"
    return m.group(1) == "CORRECT", out[:200]
