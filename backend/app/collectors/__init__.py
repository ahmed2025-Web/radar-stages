"""Collecteurs d'offres. Chaque source expose une fonction collect() -> list[Offer]."""
from .linkedin import collect as collect_linkedin
from .sample import collect as collect_sample

# Collecteurs disponibles. Ceux réellement exécutés dépendent de ACTIVE_COLLECTORS.
COLLECTORS = {
    "sample": collect_sample,
    "linkedin": collect_linkedin,
}
