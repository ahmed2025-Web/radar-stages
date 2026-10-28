"""Modèle d'offre normalisé — format commun à tous les collecteurs."""
from __future__ import annotations

import hashlib
from pydantic import BaseModel, Field


class Offer(BaseModel):
    company: str
    title: str
    url: str
    source: str = "sample"          # linkedin, wttj, jobteaser, …
    location: str = ""
    country: str = "France"
    remote: bool = False
    posted: str = ""                # texte brut ("il y a 1 semaine")
    salary: str | None = None
    tags: list[str] = Field(default_factory=list)
    description: str = ""
    apply_mode: str = "site"        # site, easy_apply, mail
    # Rempli par le pipeline :
    match: int = 0                  # score 0–100 offre ↔ profil
    applied: bool = False

    @property
    def id(self) -> str:
        """Identifiant stable pour le dédoublonnage (entreprise + intitulé + source)."""
        raw = f"{self.company}|{self.title}|{self.source}".lower().strip()
        return hashlib.sha1(raw.encode()).hexdigest()[:16]

    def match_text(self) -> str:
        """Texte représentatif de l'offre pour le scoring."""
        return " ".join([self.title, self.company, " ".join(self.tags), self.description])
