"""Collecteur LinkedIn — à implémenter.

Pistes :
  - API publique des offres (guest) : https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
  - ou scraping respectueux via une session connectée (Playwright), avec throttling.
Contrainte : rester raisonnable (pas de spam) pour ne pas se faire bloquer.
"""
from __future__ import annotations

from ..models import Offer


def collect() -> list[Offer]:
    # TODO : récupérer et normaliser les offres LinkedIn.
    raise NotImplementedError("Collecteur LinkedIn pas encore implémenté")
