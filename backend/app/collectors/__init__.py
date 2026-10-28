"""Collecteurs d'offres. Chaque source expose une fonction collect() -> list[Offer]."""
from .sample import collect as collect_sample

# Les collecteurs actifs. À compléter : linkedin, wttj, jobteaser.
COLLECTORS = {
    "sample": collect_sample,
}
