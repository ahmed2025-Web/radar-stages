"""Génération d'un brouillon de lettre de motivation adapté à une offre.

Construit un prompt à partir de l'offre et du profil (CV), puis le soumet au LLM.
La construction du prompt est séparée de l'appel réseau pour rester testable.
"""
from __future__ import annotations

from .llm import LLMClient, get_llm
from .models import Offer

_SYSTEM = (
    "Tu es un assistant qui rédige des brouillons de lettres de motivation en "
    "français pour des candidatures de stage. Tu t'appuies UNIQUEMENT sur le "
    "profil fourni : n'invente aucune expérience, aucun diplôme, aucune compétence."
)


def build_prompt(offer: Offer, profile_text: str) -> str:
    """Assemble le prompt envoyé au LLM (fonction pure, testable sans réseau)."""
    return f"""{_SYSTEM}

# Offre
Entreprise : {offer.company}
Intitulé : {offer.title}
Lieu : {offer.location or "non précisé"}
Compétences visées : {", ".join(offer.tags) or "non précisées"}
Description : {offer.description or "non fournie"}

# Profil du candidat (CV)
{profile_text}

# Tâche
Rédige un brouillon de lettre de motivation (250–300 mots) pour cette offre :
- adapte-la à l'entreprise et à l'intitulé ci-dessus,
- mets en avant les éléments du profil réellement pertinents pour cette offre,
- ton professionnel et sincère, sans formules creuses,
- n'invente rien qui ne soit pas dans le profil,
- termine par une formule de politesse.
Renvoie uniquement le texte de la lettre.
"""


def generate_cover_letter(
    offer: Offer, profile_text: str, llm: LLMClient | None = None
) -> str:
    """Génère la lettre via le LLM (Mistral par défaut)."""
    client = llm or get_llm()
    return client.generate(build_prompt(offer, profile_text))
