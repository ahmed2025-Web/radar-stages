"""Contrat commun à tous les collecteurs."""
from __future__ import annotations

from typing import Protocol

from ..models import Offer


class Collector(Protocol):
    """Un collecteur récupère les offres d'une source et les renvoie normalisées."""

    def collect(self) -> list[Offer]:
        ...


def linkedin_search_url(title: str, company: str) -> str:
    """Lien de recherche LinkedIn vers une offre (fallback quand on n'a pas l'URL exacte)."""
    from urllib.parse import quote_plus

    return "https://www.linkedin.com/jobs/search/?keywords=" + quote_plus(f"{title} {company}")
