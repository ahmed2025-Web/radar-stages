"""Configuration centrale, lue depuis l'environnement (.env)."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _path(env_value: str) -> Path:
    p = Path(env_value)
    return p if p.is_absolute() else ROOT / p


DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///data/radar.db")
PROFILE_PATH: Path = _path(os.getenv("PROFILE_PATH", "profile/cv.md"))
FRONTEND_DIR: Path = ROOT / "frontend"

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "mistral")
MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

EMBEDDING_MODEL: str = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)


def _csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


# Ce que le radar CHERCHE : défini par des mots-clés, pas par le CV. La collecte
# ratisse large ; le CV ne sert qu'au scoring (classement), jamais au filtrage.
SEARCH_KEYWORDS: list[str] = _csv(
    os.getenv(
        "SEARCH_KEYWORDS",
        "stage développement logiciel,stage software engineer,stage IA,"
        "stage machine learning,stage data,stage full stack",
    )
)
SEARCH_LOCATIONS: list[str] = _csv(os.getenv("SEARCH_LOCATIONS", "France"))
SEARCH_INTERNATIONAL: bool = os.getenv("SEARCH_INTERNATIONAL", "false").lower() == "true"

# Collecteurs exécutés par le pipeline. "sample" seul par défaut (aucun réseau) ;
# ajoute "linkedin" pour activer le scraping réel : ACTIVE_COLLECTORS=sample,linkedin
ACTIVE_COLLECTORS: list[str] = _csv(os.getenv("ACTIVE_COLLECTORS", "sample"))


def sqlite_path() -> Path:
    """Chemin du fichier SQLite déduit de DATABASE_URL (sinon data/radar.db)."""
    if DATABASE_URL.startswith("sqlite:///"):
        return _path(DATABASE_URL.removeprefix("sqlite:///"))
    return ROOT / "data" / "radar.db"


def read_profile() -> str:
    """Contenu du CV / profil utilisé pour le matching et la génération de lettre."""
    try:
        return PROFILE_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""
