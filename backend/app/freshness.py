"""Détermine si une offre est « nouvelle » d'après sa date de première détection."""
from __future__ import annotations

from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def is_new(first_seen: str, window_hours: int) -> bool:
    """True si `first_seen` (ISO) est à moins de `window_hours` de maintenant."""
    if not first_seen:
        return False
    try:
        seen = datetime.fromisoformat(first_seen)
    except ValueError:
        return False
    if seen.tzinfo is None:
        seen = seen.replace(tzinfo=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - seen).total_seconds() / 3600
    return 0 <= age_hours <= window_hours
