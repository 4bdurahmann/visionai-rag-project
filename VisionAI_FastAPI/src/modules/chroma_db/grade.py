"""
Medical RAG - Shared recommendation-grade extraction
----------------------------------------------------
USPSTF recommendation chunks carry a grade badge (A/B/C/D/I). Two forms appear
in parsed text:
  - explicit: "Grade: B"
  - bare: the grade sometimes parses as a lone letter at end of a line,
    e.g. "...activity. B"
"""

import re

_GRADE_EXPLICIT_RE = re.compile(r"\bGrade[:：]?\s*\*?([ABCDI])\*?")
_GRADE_BARE_RE = re.compile(r"\.\s*\n?\s*([ABCDI])\s*(?=\n|$)")


def extract_grade(text: str) -> str | None:
    m = _GRADE_EXPLICIT_RE.search(text)
    if m:
        return m.group(1).upper()
    m = _GRADE_BARE_RE.search(text)
    return m.group(1).upper() if m else None
