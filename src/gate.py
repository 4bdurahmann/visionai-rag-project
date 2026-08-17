"""
Medical RAG - Confidence / coverage gating
------------------------------------------
Decides whether a query is confidently covered by the guideline corpus, i.e.
whether the "I'm just a demo medical chatbot" disclaimer should be shown.

Three gates, first to fire wins:
  1. Similarity gate - if the best matching chunk's vector similarity is below
     a threshold, the query is likely unrelated to the corpus.
  2. Fusion gate - if no chunk ranked well in BOTH the vector and BM25
     rankings (top fused RRF score below a threshold), the query shares no
     meaningful keywords with any source text.
  3. Grade gate (decision-style queries only) - recommendation grades
     (A/B/C/D/I) only appear in recommendation chunks, so a clinical-decision
     question ("should my patient...", "what grade for X") whose topic is not
     addressed by any graded chunk is probably outside the corpus.

Notes / limits:
  - Factual questions (harms, importance, evidence) legitimately have no grade,
    so the grade gate is only applied to decision-style questions.
  - A topic-adjacent question can still surface a generic graded chunk
    (e.g. a statin question returning the counseling recommendation), so the
    grade gate is a heuristic, not a guarantee.
"""

import re

DEFAULT_SIM_THRESHOLD = 0.30
# A fused (RRF) score of ~0.0164 means the top chunk ranked in only ONE of the
# two rankings (vector or BM25). If it ranked in both, the score is >= ~0.026.
# A top chunk sitting below ~0.020 therefore has no keyword overlap -- a strong
# out-of-source signal even when similarity looks moderate.
FUSED_THRESHOLD = 0.020
# The grade gate looks this far down the ranking (independent of how many hits
# are shown) so that a graded recommendation chunk, if one exists, is found.
GRADE_LOOKAHEAD = 10
# A graded chunk only satisfies the grade gate if it actually addresses the
# question's topic: it must share at least this many content (non-stop) words
# with the query. Otherwise the grade belongs to a different recommendation.
MIN_GRADE_TOPIC_OVERLAP = 3

DISCLAIMER_LOW_SIM = (
    "I'm just a demo medical chatbot. I couldn't find a confident match "
    "for your question in the guideline sources I cover (best match similarity "
    "is only {sim:.1f}%). This question may be outside the sources, so I can't "
    "give a reliable answer -- please consult a clinician or check the "
    "USPSTF/CDC/WHO guideline directly."
)

DISCLAIMER_LOW_FUSION = (
    "I'm just a demo medical chatbot. I couldn't find a confident match "
    "for your question in the guideline sources I cover (the closest source "
    "text shares no meaningful keywords with it). This question may be outside "
    "the sources, so I can't give a reliable answer -- please consult a "
    "clinician or check the USPSTF/CDC/WHO guideline directly."
)

DISCLAIMER_NO_GRADE = (
    "I'm just a demo medical chatbot. This looks like a clinical "
    "recommendation question, but I couldn't find a graded recommendation "
    "(A/B/C/D/I) covering it in the guideline sources I cover, so I can't "
    "give a reliable answer -- please consult a clinician or check the "
    "USPSTF/CDC/WHO guideline directly."
)

# Decision-style questions: asking whether *to do* something for a patient, or
# what grade applies to a specific intervention/condition. Kept narrow on
# purpose so that factual questions that merely mention words like
# "recommendation" or "should" ("does this recommendation apply to...?",
# "how much physical activity should the counseling aim for?") are NOT gated.
DECISION_RE = re.compile(
    r"\b(should|ought|can|could|do i|do i need|does my|would you|"
    r"is it (advisable|worth|safe))\b"
    r".*?\b(i|we|my|me|the patient|my patient|patients|someone|a patient|"
    r"an adult|women|pregnant women|individuals|people|one)\b"
    r"|"
    r"\b(grade|rating)\b.*\b(for|of|about|regarding|give|gives|given)\b"
    r"|"
    r"\b(recommend(ed|s)?|recommendation)\b.*\b(for|against)\b",
    re.IGNORECASE,
)


def is_decision_query(text: str) -> bool:
    return bool(DECISION_RE.search(text))


# Common words excluded from the topic-overlap check so that queries like
# "take a statin" vs a chunk about "behavioral counseling" are judged by their
# real clinical content rather than by "the/a/of/with".
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "if", "then", "else", "for", "to",
    "of", "in", "on", "with", "at", "by", "from", "as", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "will", "would", "can", "could", "should", "may", "might", "must", "not",
    "no", "so", "that", "this", "these", "those", "it", "its", "i", "you",
    "we", "they", "he", "she", "their", "them", "me", "my", "your", "what",
    "how", "why", "who", "when", "which", "about", "more", "most", "into",
    "does", "take", "get", "give", "given", "aim", "offer", "offering",
    "use", "using", "help", "helps",
}


def _content_tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (text or "").lower())) - _STOPWORDS


def _graded_chunk_addresses_query(query_text: str, hits) -> bool:
    """True if some retrieved graded chunk shares enough clinical content with
    the question to be considered the relevant graded recommendation."""
    query_tokens = _content_tokens(query_text)
    if not query_tokens:
        return True
    for _cid, _sim, _fused, doc, meta in hits:
        if not meta.get("grade"):
            continue
        overlap = len(_content_tokens(doc) & query_tokens)
        if overlap >= MIN_GRADE_TOPIC_OVERLAP:
            return True
    return False


def disclaim(query_text, hits, sim_threshold: float = DEFAULT_SIM_THRESHOLD,
             fused_threshold: float = FUSED_THRESHOLD,
             use_grade_gate: bool = True):
    """
    Decide whether the disclaimer should be shown.

    hits: list of (cid, sim, fused, doc, meta) as returned by retrieval.search.

    Returns (message_or_None, reason) where reason is
    "low_similarity", "low_fusion", "no_grade_for_decision", or "none".
    """
    sims = [sim for _, sim, _, _, _ in hits]
    fusions = [fused for _, _, fused, _, _ in hits]
    top_sim = max(sims) if sims else 0.0
    top_fused = max(fusions) if fusions else 0.0

    if top_sim < sim_threshold:
        return DISCLAIMER_LOW_SIM.format(sim=top_sim * 100), "low_similarity"

    if top_fused < fused_threshold:
        return DISCLAIMER_LOW_FUSION, "low_fusion"

    if use_grade_gate and is_decision_query(query_text):
        if not _graded_chunk_addresses_query(query_text, hits):
            return DISCLAIMER_NO_GRADE, "no_grade_for_decision"

    return None, "none"