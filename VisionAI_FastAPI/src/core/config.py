"""
Project-wide configuration.

Adopts the friend's pydantic-settings ``Settings``/``get_settings()`` pattern
(project metadata + API keys read from the project-root ``.env``), while
keeping the path constants every module depends on (``DATA_DIR``,
``DEFAULT_DB``, ``MODEL_NAME`` ...) and the minimal ``load_env()`` seeding.

Metadata fields are optional with defaults so the server never 500s when
``.env`` is incomplete; the rest of the codebase reads secrets through
``os.environ`` (as seeded by ``load_env()`` / ``Settings``).
"""

import os
from pathlib import Path

from pydantic_settings import BaseSettings

# --- layout ---------------------------------------------------------------
#   <project root>/           .env
#   <project root>/src/      core/config.py, data/, modules/...
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
ENV_FILE = PROJECT_ROOT / ".env"

# --- data -----------------------------------------------------------------
DATA_DIR = SRC_DIR / "data"
CHROMA_DIR = SRC_DIR / "modules" / "chroma_db" / "chroma_data"
DEFAULT_DB = str(CHROMA_DIR)
COLLECTION = "guidelines"

# --- source documents & artifacts -----------------------------------------
SOURCE_DOC_JSON = str(DATA_DIR / "healthy-diet-phys-activity-high-risk-final-rec.json")
SOURCE_DOC_PDF = str(SRC_DIR / "assets" / "healthy-diet-phys-activity-high-risk-final-rec.pdf")
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


class Settings(BaseSettings):
    """Environment-backed settings, mirroring the friend's project config.

    All fields are optional with safe defaults so an incomplete ``.env`` never
    breaks the server. List fields accept JSON in the env var, e.g.
    ``PROJECT_ORGANIZERS=["Org A","Org B"]``.
    """

    PROJECT_NAME:str
    PROJECT_EVENT:str
    PROJECT_ORGANIZERS:list
    PROJECT_INSTRUCTORS:list
    SUPERVISOR_TEAM:str
    SUPERVISOR_MEMBER:list
    PROJECT_DATE:str
    LLAMAPARSE_APIKEY:str
    GROQ_API_KEY:str
    GROQ_MODEL:str

    # PROJECT_NAME: str = "VisionAI Medical RAG"
    # PROJECT_EVENT: str = "USPSTF Guideline Q&A"
    # PROJECT_ORGANIZERS: list[str] = []
    # PROJECT_INSTRUCTORS: list[str] = []
    # SUPERVISOR_TEAM: str = "Clinical Advisory Team"
    # SUPERVISOR_MEMBER: list[str] = []
    # PROJECT_DATE: str = ""
    # LLAMAPARSE_APIKEY: str = ""
    # GROQ_API_KEY: str = ""
    # GROQ_MODEL: str = "openai/gpt-oss-120b"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()



# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     PROJECT_NAME:str
#     PROJECT_EVENT:str
#     PROJECT_ORGANIZERS:list
#     PROJECT_INSTRUCTORS:list
#     SUPERVISOR_TEAM:str
#     SUPERVISOR_MEMBER:list
#     PROJECT_DATE:str
#     LLAMAPARSE_APIKEY:str
#     GROQ_API_KEY:str
#     GROQ_MODEL:str
    
#     class Config:
#         env_file = ".env"



# def get_settings():
#     return Settings()
