"""
Project-wide configuration.

Central place for paths, constants, and the minimal .env loader (no external
dependency). Every module that needs paths or secrets imports this instead of
hardcoding ``Parent / "data" / ...`` relative paths or reading keys itself.

Secrets are read from the project-root ``.env`` file (never committed) with
``load_env()``; already-set environment variables always win.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"

# --- data -----------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = DATA_DIR / "chroma"
DEFAULT_DB = str(CHROMA_DIR)
COLLECTION = "guidelines"

# --- source documents & artifacts -----------------------------------------
SOURCE_DOC_JSON = str(DATA_DIR / "healthy-diet-phys-activity-high-risk-final-rec.json")
SOURCE_DOC_PDF = str(DATA_DIR / "healthy-diet-phys-activity-high-risk-final-rec.pdf")
EMBEDDED_CHUNKS = str(DATA_DIR / "embedded_chunks.json")
EVAL_QUESTIONS = str(DATA_DIR / "eval_questions.json")
ACCURACY_JSON = str(DATA_DIR / "accuracy_results.json")

# --- models ---------------------------------------------------------------
MODEL_NAME = "NeuML/pubmedbert-base-embeddings"


def load_env() -> None:
    """Minimal ``KEY=VALUE`` loader for the project-root ``.env``.

    Uses ``os.environ.setdefault`` so variables exported in the shell are never
    overridden by the file.
    """
    import os

    try:
        with open(ENV_FILE, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())
    except OSError:
        print(f"[config] WARNING: could not read {ENV_FILE}")


load_env()