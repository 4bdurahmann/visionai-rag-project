"""
Medical RAG - LLM integration (Groq with OpenAI fallback)
----------------------------------------------------------
Jobs:
  1. generate_answer      - turn the retrieved chunks into a natural-language
                            answer that cites sources inline as 【N】 markers.
  2. judge_answer         - evaluate (in evaluate_accuracy.py) whether the
                            retrieved chunks are sufficient to answer a
                            ground-truth question.
  3. grade_refusal        - self-grade a refusal against the 3-point rubric.
  4. score_faithfulness   - supported claims / total claims made, judged
                            against the retrieved evidence (hallucination).
  5. score_citation_accuracy - citations correct / citations given, where a
                            citation is correct only if it resolves to a real
                            source excerpt, that excerpt has accurate
                            section+page provenance, and it genuinely supports
                            the sentence it is attached to.

Providers: the active one is chosen by LLM_PROVIDER = openrouter | gemini |
alibaba | groq | openai | auto (default). Auto picks the first available key in
that same order. All OpenAI-style providers (openai, gemini, openrouter,
alibaba) use the OpenAI SDK with their base URL; Groq uses the groq SDK. If Groq
hits its daily token quota (HTTP 429 "tokens per day"), the request
automatically fails over to the next available provider and every later call
skips Groq for the rest of the process. Keys are never hardcoded.
"""

"""LLM integration: provider selection, answer generation, and quality scoring.

Imported by the query pipeline and the CLI tools. Importing this module loads
the project .env so API keys are available without extra setup.
"""

import os
import re
import time
from typing import Literal

from groq import Groq
from groq import APIError as GroqAPIError

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - only needed when falling back
    OpenAI = None  # type: ignore[assignment]

# --- portable .env loading ------------------------------------------------
# Locate the project-root .env relative to THIS file with os.path.join /
# os.path.abspath (the same self-contained method the friend's llm.py uses),
# so the module resolves the correct .env on any machine or launch directory.
_ENV_FILE = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")
)


def _load_dotenv(path: str = _ENV_FILE) -> None:
    """Minimal ``KEY=VALUE`` loader for the project-root ``.env``."""
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
    except OSError:
        pass


_load_dotenv()

Provider = Literal["groq", "openai", "gemini", "openrouter", "alibaba"]

DEFAULT_MODEL = "openai/gpt-oss-120b"
# Judges ideally run on a DIFFERENT model than the answer generator so a model
# is never grading its own output. Default to a separate model when it has
# quota; override with GROQ_JUDGE_MODEL. (Temporarily same as generator while
# the smaller judge model is quota-exhausted on this key/org.)
DEFAULT_JUDGE_MODEL = "openai/gpt-oss-120b"

# OpenAI fallback (used when Groq's TPD quota is exhausted). Cheap + reliable;
# override the models with OPENAI_MODEL / OPENAI_JUDGE_MODEL.
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_OPENAI_JUDGE_MODEL = "gpt-4o-mini"
# Retry 429 (rate limit) / timeouts / connection errors only briefly. A short
# backoff absorbs one-off transient blips, but a genuinely exhausted quota 429s
# forever, so we must NOT stall the request for minutes: fail fast instead and
# let the API degrade gracefully. Total worst-case added sleep: ~2+4=6s.
_MAX_RETRIES = 3
_BASE_RETRY_SECONDS = 2

_SYSTEM_ANSWER = (
    "You are a medical Q&A assistant over USPSTF/CDC/WHO clinical guideline "
    "documents. Answer the user's question directly and specifically using ONLY "
    "the provided source excerpts. Give the concrete facts the excerpts "
    "actually state - numbers, letter grades, populations, interventions, "
    "recommended actions. Do NOT open with boasts like 'The available source "
    "excerpts do not provide evidence...' or otherwise hedge against answering: "
    "assume the excerpts are relevant and answer from them, unless every excerpt "
    "genuinely fails to address the question.\n\n"
    "Each source excerpt is labelled with the document, section, page number, "
    "recommendation grade, and issuing organization. Cite your sources inline: "
    "after every factual statement append one or more citation markers of the "
    "form 【N】 matching the excerpt numbers below (e.g. 【1】【3】). Cite only "
    "excerpts that genuinely support what you state, and attach markers only "
    "to the specific excerpt(s) that back each statement - never cite a "
    "tangential or generic excerpt. Prefer the fewest, most specific markers. "
    "Be concise and factual.\n\n"
    "Only when the information needed to answer is genuinely absent from every "
    "excerpt, refuse honestly and briefly: (1) plainly state the excerpts do not "
    "provide evidence for this question; (2) do NOT invent a statistic, "
    "confidence level, citation, or reference; (3) end with a concrete next "
    "step, e.g. rephrase the question, consult a clinician, or check the "
    "USPSTF/CDC/WHO guideline directly."
)

_SYSTEM_JUDGE = (
    "You are evaluating a medical RAG retrieval system. You are given a "
    "question, the ground-truth expected answer, and the source excerpts the "
    "system retrieved. Reply on a single line starting with exactly 'CORRECT' "
    "or 'INCORRECT', followed by a short reason. Judge CORRECT only if the "
    "retrieved excerpts actually contain the information needed to answer the "
    "question; partial or off-topic excerpts are INCORRECT."
)

_SYSTEM_REFUSAL_GRADER = (
    "You grade the quality of a medical AI refusal message on a 3-point rubric.\n"
    "Rubric (score 1 point per satisfied criterion):\n"
    "1. States insufficiency: clearly says the available evidence/sources do "
    "not support an answer, with no vague hedging and no partial guess.\n"
    "2. Stays honest: does not fabricate a confidence level, statistic, "
    "citation, or reference to sound credible.\n"
    "3. Offers a next step: suggests something concrete - rephrasing the "
    "question, consulting a clinician, or checking a different source.\n"
    "Reply on a single line: 'X/3 criteria' followed by one short reason "
    "per missed criterion."
)

_SYSTEM_CLAIM_EXTRACT = (
    "You are decomposing a medical RAG answer into its atomic factual claims. "
    "Split the answer into the smallest standalone statements that each assert "
    "a distinct fact (e.g. a specific number, rate, recommendation, or causal "
    "claim). Ignore conversational padding, citation markers, and non-factual "
    "sentences. Output each claim on its own line starting with 'CLAIM: '. "
    "No numbering, no headers, no commentary outside the CLAIM lines."
)

_SYSTEM_CLAIM_JUDGE = (
    "You are checking whether the claims in a medical RAG answer are supported "
    "by the retrieved source excerpts. A claim is SUPPORTED only if the "
    "information it asserts can be inferred from at least one provided excerpt. "
    "If a claim restates a source fact or a genuine implication of one, mark it "
    "SUPPORTED; otherwise (wrong number, invented stat, unsupported conclusion, "
    "or a detail found nowhere in the excerpts) mark it UNSUPPORTED.\n"
    "Output one line per claim, EXACTLY: 'N SUPPORTED' or 'N UNSUPPORTED', "
    "where N is the claim number given below. No other text."
)

_SYSTEM_CITATION_JUDGE = (
    "You are checking citation attribution in a medical RAG answer. You are "
    "given a list of citation items. Each item K contains a sentence from the "
    "answer, a citation marker 【M】 used in it, and the source excerpt that "
    "marker refers to. For each item, decide whether THAT specific excerpt "
    "actually supports the sentence's factual claim (precision of "
    "attribution). A marker is SUPPORTED only if the excerpt genuinely backs "
    "the sentence; if it is tangential, generic, or contradicts the sentence, "
    "mark it UNSUPPORTED.\n"
    "Output one line per item, EXACTLY: 'K SUPPORTED' or 'K UNSUPPORTED', "
    "where K is the item number given below. No other text."
)


def get_client() -> Groq:
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        raise RuntimeError(
            "GROQ_API_KEY is not set - export it first, e.g. "
            "export GROQ_API_KEY=gsk_..."
        )
    # 60s client timeout so a hung connection fails fast instead of blocking
    # the endpoint indefinitely.
    return Groq(api_key=key, timeout=60.0)


def model_name() -> str:
    return os.environ.get("GROQ_MODEL", DEFAULT_MODEL)


def judge_model_name() -> str:
    return os.environ.get("GROQ_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)


_groq_quota_out = False


def _is_rate_limited(exc: Exception) -> bool:
    return isinstance(exc, GroqAPIError) and (
        "429" in str(exc) or "rate limit" in str(exc).lower()
    )


# OpenAI-style providers: same API shape, just a different key + base URL.
# models = (generator default, judge default); override per provider with
# <PROVIDER>_MODEL / <PROVIDER>_JUDGE_MODEL env vars (e.g. OPENROUTER_MODEL).
_OPENAI_STYLE = {
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "base_url": None,
        "models": (DEFAULT_OPENAI_MODEL, DEFAULT_OPENAI_JUDGE_MODEL),
    },
    "gemini": {
        "key_env": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "models": ("gemini-2.5-flash", "gemini-2.5-flash"),
    },
    "openrouter": {
        "key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "models": ("gpt-4o-mini", "gpt-4o-mini"),
    },
    "alibaba": {
        "key_env": "ALIBABA_API_KEY",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "models": ("qwen-plus", "qwen-plus"),
    },
}
# Autodetect priority when LLM_PROVIDER is not set.
_PRIORITY: list[str] = ["openrouter", "gemini", "alibaba", "groq", "openai"]


def _has_key(provider: str) -> bool:
    if provider == "groq":
        return bool(os.environ.get("GROQ_API_KEY"))
    return bool(os.environ.get(_OPENAI_STYLE[provider]["key_env"]))


def _provider() -> Provider:
    """Resolve the active provider: env override, else autodetect."""
    p = os.environ.get("LLM_PROVIDER", "auto").strip().lower()
    if p in _PRIORITY:
        return p  # type: ignore[return-value]
    for cand in _PRIORITY:
        if _has_key(cand):
            return cand  # type: ignore[return-value]
    raise RuntimeError(
        "No LLM provider configured - set one of "
        "OPENROUTER_API_KEY, GEMINI_API_KEY, ALIBABA_API_KEY, GROQ_API_KEY, "
        "OPENAI_API_KEY, or force one with LLM_PROVIDER="
        + "|".join(_PRIORITY)
    )


def _resolve_model(provider: Provider, judge: bool = False) -> str:
    if provider == "groq":
        return judge_model_name() if judge else model_name()
    cfg = _OPENAI_STYLE[provider]
    env = (f"{provider.upper()}_MODEL", f"{provider.upper()}_JUDGE_MODEL")
    override = os.environ.get(env[1] if judge else env[0])
    return override or (cfg["models"][1] if judge else cfg["models"][0])


def _openai_style_client(provider: Provider) -> OpenAI:
    cfg = _OPENAI_STYLE[provider]
    key = os.environ.get(cfg["key_env"])
    if not key or OpenAI is None:
        raise RuntimeError(f"{provider} configured but {cfg['key_env']} is not set")
    return OpenAI(api_key=key, base_url=cfg["base_url"], timeout=60.0)


def _provider_call(provider: Provider, system: str, user: str,
                   judge: bool = False, temperature: float = 0.2) -> str:
    """One LLM completion on a single provider (no fallback)."""
    if provider == "groq":
        return _groq_call(system, user, judge=judge, temperature=temperature)
    resp = _openai_style_client(provider).chat.completions.create(
        model=_resolve_model(provider, judge=judge),
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def _groq_call(system: str, user: str, judge: bool = False,
               temperature: float = 0.2) -> str:
    """Groq completion with brief retries. Rate limits are NOT retried here -
    they bubble up so the caller can fail over to another provider."""
    client = get_client()
    model = _resolve_model("groq", judge=judge)
    last_exc: Exception | None = None
    for attempt in range(_MAX_RETRIES):
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return (resp.choices[0].message.content or "").strip()
        except GroqAPIError as exc:
            last_exc = exc
            if _is_rate_limited(exc):
                raise  # fail over in _chat, do not burn retries
            raise
        except (TimeoutError, ConnectionError) as exc:
            last_exc = exc
            msg = str(exc)
            if "timed out" not in msg.lower() and "connection" not in msg.lower():
                raise
            if attempt == _MAX_RETRIES - 1:
                break
            time.sleep(min(_BASE_RETRY_SECONDS * (2 ** attempt), 300))
    raise last_exc  # type: ignore[misc]


def _chat(system: str, user: str, temperature: float = 0.2,
          judge: bool = False) -> str:
    """Single LLM completion with provider fallback.

    Primary provider chosen by LLM_PROVIDER env or autodetect (priority:
    openrouter, gemini, alibaba, groq, openai). If Groq reports its daily TPD
    quota is gone, the current AND all later calls fail over to the next
    available provider. Never retries a rate limit repeatedly - it fails over.
    An error on the primary non-Groq provider propagates (do not silently
    mask real config/key problems).
    """
    global _groq_quota_out
    primary = _provider()
    chain = [primary]
    if primary == "groq":
        chain += [p for p in _PRIORITY if p != "groq" and _has_key(p)]
    last_exc: Exception | None = None
    for p in chain:
        try:
            return _provider_call(p, system, user, judge=judge, temperature=temperature)
        except GroqAPIError as exc:
            last_exc = exc
            if _is_rate_limited(exc):
                _groq_quota_out = True
                continue  # try the next provider in the chain
            raise
    raise last_exc  # type: ignore[misc]


def _excerpts(hits) -> str:
    lines = []
    for i, (_cid, _sim, _fused, doc, meta) in enumerate(hits, 1):
        heading = meta.get("heading") or "untitled section"
        org = meta.get("org") or "?"
        grade = meta.get("grade")
        grade_str = f", Grade {grade}" if grade else ""
        doc_title = meta.get("doc_title") or meta.get("doc_id") or "guideline"
        page = meta.get("page")
        page_str = f" p.{page}" if page is not None else ""
        lines.append(
            f"[{i}] Doc: {doc_title} | Section: {heading} | {org}{page_str}{grade_str}\n"
            f"{doc[:1500]}"
        )
    return "\n\n".join(lines)


def generate_answer(query_text: str, hits) -> str:
    """Natural-language answer over the retrieved chunks (RAG generation)."""
    user = (
        f"Question: {query_text}\n\n"
        f"Source excerpts (top {len(hits)} retrieved chunks):\n{_excerpts(hits)}"
    )
    return _chat(_SYSTEM_ANSWER, user)


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
        out = _chat(_SYSTEM_JUDGE, user, judge=True)
    except Exception as exc:  # noqa: BLE001 - report any API error to the caller
        return None, f"llm error: {exc}"

    m = re.match(r"\b(CORRECT|INCORRECT)\b", out.upper())
    if not m:
        return None, f"unparseable LLM verdict: {out[:120]!r}"
    return m.group(1) == "CORRECT", out[:200]


def grade_refusal(message: str) -> tuple[float | None, str]:
    """Self-grade a refusal message against the 3-point rubric.
    Returns (score 0-3, reason); on any API/config error returns (None, error)."""
    try:
        user = f"Refusal message to grade:\n\n{message}"
        out = _chat(_SYSTEM_REFUSAL_GRADER, user, judge=True)
    except Exception as exc:  # noqa: BLE001 - report any API error to the caller
        return None, f"llm error: {exc}"

    m = re.search(r"([0-3])\s*/\s*3", out)
    if not m:
        return None, f"unparseable refusal score: {out[:120]!r}"
    return int(m.group(1)), out[:200]


_CITE_RE = re.compile(r"【(\d+)】(?:【(\d+)】)*")


def _split_claims(answer: str) -> list[str]:
    """Naive fallback claim splitter used if the LLM extractor is unavailable."""
    parts = re.split(r"[.;]\s+|\n+", answer)
    return [p.strip() for p in parts if len(p.strip()) > 15]


def extract_claims(answer: str) -> tuple[list[str], str]:
    """Split an answer into its atomic factual claims.

    Uses the LLM extractor when possible; falls back to naive sentence
    splitting so scoring never hard-fails on a transient API error.
    Returns (claims, status) where status is an empty string on success or a
    short note when a fallback or error occurred.
    """
    try:
        out = _chat(_SYSTEM_CLAIM_EXTRACT, f"Answer:\n\n{answer}", judge=True)
        claims = [
            re.sub(r"^CLAIM\s*:\s*", "", ln.strip(), flags=re.I)
            for ln in out.splitlines()
            if ln.strip().upper().startswith("CLAIM")
        ]
        claims = [c for c in claims if c]
        if claims:
            return claims, ""
        return _split_claims(answer), "fallback: LLM returned no CLAIM lines"
    except Exception as exc:  # noqa: BLE001
        return _split_claims(answer), f"fallback: extractor error ({exc})"


def score_faithfulness(answer: str, hits: list) -> tuple[float | None, dict]:
    """Faithfulness = supported claims / total claims made.

    Each atomic claim in the answer is judged against the retrieved evidence;
    a claim is UNSUPPORTED if no excerpt supports it (the hallucination signal).
    Answers with no claims at all (e.g. refusals) are n/a -> (None, details).
    Never raises: returns (None, {.. 'error': ..}) on any API/config problem.
    """
    claims, status = extract_claims(answer)
    if not claims:
        return None, {
            "n_claims": 0,
            "error": status or "no claims to score (refusal/non-factual answer)",
        }

    numbered = "\n".join(f"{i + 1}. {c}" for i, c in enumerate(claims))
    user = (
        f"Numbered claims:\n{numbered}\n\n"
        f"Retrieved source excerpts:\n{_excerpts(hits)}\n\n"
        "Verdict for each claim, one per line: 'N SUPPORTED' or 'N UNSUPPORTED'."
    )
    try:
        out = _chat(_SYSTEM_CLAIM_JUDGE, user, judge=True)
    except Exception as exc:  # noqa: BLE001
        return None, {"n_claims": len(claims), "error": f"llm error: {exc}"}

    verdicts: dict[int, bool] = {}
    for n, v in re.findall(r"(\d+)\s+(SUPPORTED|UNSUPPORTED)", out.upper()):
        verdicts[int(n)] = v == "SUPPORTED"

    supported, unsupported = [], []
    for i, claim in enumerate(claims, 1):
        ok = verdicts.get(i, False)  # missing verdict counts as UNSUPPORTED
        (supported if ok else unsupported).append(claim)

    score = round(len(supported) / len(claims), 4)
    return score, {
        "n_claims": len(claims),
        "n_supported": len(supported),
        "unsupported_claims": unsupported,
        "error": status or "",
    }


def score_citation_accuracy(answer: str, hits: list) -> tuple[float | None, dict]:
    """Citations correct / citations given.

    A citation 【N】 is CORRECT when all three of the rubric hold:
      1. it resolves to a real source excerpt (document exists in the library),
      2. that excerpt carries a valid section + page (accurate provenance),
      3. the cited excerpt actually supports the sentence it is attached to
         (checked by the LLM citation judge).
    Fabricated / out-of-range markers fail condition 1; missing provenance
    fails condition 2; a judge denial fails condition 3. All judge-able
    citations for the answer are checked in ONE batched LLM call.
    Returns (None, details) when the answer contains no citations (n/a).
    """
    sentences = [
        s.strip() for s in re.split(r"(?<=[.!?。])\s+|\n+", answer or "") if s.strip()
    ]
    cites: list[tuple[int, str]] = []  # (marker, sentence)
    for sent in sentences:
        for m in re.finditer(r"【(\d+)】", sent):
            cites.append((int(m.group(1)), sent))
    if not cites:
        return None, {"n_citations": 0, "error": "no citation markers in answer"}

    total = len(cites)
    correct = 0
    bad: list[dict] = []
    judgeable: list[dict] = []  # {k, marker, sentence, excerpt}

    for marker, sent in cites:
        # condition 1 + 2: marker resolves to a real chunk with provenance
        if not 1 <= marker <= len(hits):
            bad.append({"marker": marker, "sentence": sent[:120],
                        "reason": "no such excerpt (fabricated citation)"})
            continue
        meta = hits[marker - 1][4]
        if not (meta.get("heading") and meta.get("page") is not None):
            bad.append({"marker": marker, "sentence": sent[:120],
                        "reason": "excerpt missing section/page (bad provenance)"})
            continue
        judgeable.append({"k": len(judgeable) + 1, "marker": marker,
                          "sentence": sent, "excerpt": hits[marker - 1][3]})

    if judgeable:
        items = []
        for it in judgeable:
            items.append(
                f"Item {it['k']}. Sentence: {it['sentence']}\n"
                f"  Citation marker 【{it['marker']}】 refers to this excerpt:\n"
                f"  {it['excerpt'][:1000]}"
            )
        user = (
            f"Citation items to check (all from the same answer):\n"
            f"{chr(10).join(items)}\n\n"
            "Verdict for each item K, one per line: 'K SUPPORTED' or "
            "'K UNSUPPORTED' (is that excerpt genuinely evidence for its sentence?)."
        )
        try:
            out = _chat(_SYSTEM_CITATION_JUDGE, user, judge=True)
        except Exception as exc:  # noqa: BLE001
            return None, {"n_citations": total, "error": f"llm error: {exc}"}

        verdicts = {int(k): v == "SUPPORTED"
                    for k, v in re.findall(r"(\d+)\s+(SUPPORTED|UNSUPPORTED)", out.upper())}
        for it in judgeable:
            if verdicts.get(it["k"], False):
                correct += 1
            else:
                bad.append({"marker": it["marker"], "sentence": it["sentence"][:120],
                            "reason": "judge: cited excerpt does not support the sentence"})

    score = round(correct / total, 4)
    return score, {"n_citations": total, "n_correct": correct, "bad_citations": bad}
