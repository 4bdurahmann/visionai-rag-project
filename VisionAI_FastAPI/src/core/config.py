"""
Project-wide configuration.

Keeps the pydantic-settings ``Settings``/``get_settings()`` pattern (project
metadata + API keys read from the project-root ``.env``) and the minimal
``load_env()`` seeding.

Paths are intentionally NOT stored here. Every module resolves the ones it
needs relative to its own file with ``os.path.join`` / ``os.path.abspath``
(the same portable style as the friend's ``llm.py``), so the project runs on
any machine regardless of where it is installed.
"""

import os

from pydantic_settings import BaseSettings

# --- .env location (resolved relative to this file) -----------------------
ENV_FILE = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".env")
)


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


# --- non-path settings ----------------------------------------------------
MODEL_NAME = "NeuML/pubmedbert-base-embeddings"
COLLECTION = "guidelines"


def select_device() -> str:
    """Pick the torch device for the local embedding model.

    Defaults to CPU so the server runs identically on any machine (no CUDA /
    MPS driver required - the PubMedBERT model is small and CPU is plenty).
    Override with ``DEVICE=cuda`` / ``DEVICE=mps`` in ``.env`` when you want
    the model on a GPU, or ``DEVICE=cpu`` to force CPU.
    """
    device = os.environ.get("DEVICE", "").strip().lower()
    return device if device in {"cuda", "mps", "cpu"} else "cpu"


class Settings(BaseSettings):
    """Environment-backed settings, mirroring the friend's project config.

    All metadata fields are optional with safe defaults so an incomplete
    ``.env`` never breaks the server. List fields accept JSON in the env var,
    e.g. ``PROJECT_ORGANIZERS=["Org A","Org B"]``.
    """
    PROJECT_NAME: str = "VisionAI Medical RAG"
    PROJECT_EVENT: str = "USPSTF Guideline Q&A"
    PROJECT_ORGANIZERS: list = []
    PROJECT_INSTRUCTORS: list = []
    SUPERVISOR_TEAM: str = "Clinical Advisory Team"
    SUPERVISOR_MEMBER: list = []
    PROJECT_DATE: str = ""
    LLAMAPARSE_APIKEY: str = ""
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    class Config:
        # Absolute path so metadata/secrets resolve from any launch directory.
        env_file = str(ENV_FILE)
        env_file_encoding = "utf-8"
        extra = "ignore"


def get_settings() -> Settings:
    return Settings()
