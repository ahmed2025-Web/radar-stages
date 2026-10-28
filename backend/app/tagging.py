"""Inférence de tags techno à partir de l'intitulé d'une offre.

Règles à base d'expressions régulières avec limites de mots (\\b), pour éviter
les faux positifs (ex. « ai » ne doit pas matcher « email » ou « travail »).
Les tags les plus spécifiques sont listés avant « Dev », et on en garde 4 au plus.
"""
from __future__ import annotations

import re

# Ordre = priorité d'affichage (du plus spécifique au plus générique).
_RULES: dict[str, str] = {
    "IA": r"\b(ia|ai|intelligence artificielle|machine learning|deep learning|ml|mlops|nlp|gen\s?ai|genai|llm|agent(?:ique|s)?)\b",
    "Data": r"\b(data|données|analytics|big data)\b",
    "Full-Stack": r"\bfull[\s-]?stack\b",
    "Web": r"\b(web|front[\s-]?end|react|angular|vue)\b",
    "Backend": r"\b(back[\s-]?end|micro[\s-]?services?|api)\b",
    "Java": r"\bjava\b",
    "Python": r"\bpython\b",
    "DevOps": r"\b(devops|cloud|kubernetes|docker|ci[\s/]?cd|mlops)\b",
    "Mobile": r"\b(mobile|android|ios|kotlin|swift|flutter|react native)\b",
    "Cybersécurité": r"\b(cyber\w*|sécurité|security)\b",
    "Conseil": r"\b(consultant\w*|conseil|consulting)\b",
    "Dev": r"\b(d[ée]velopp\w*|developer|software|engineer|ing[ée]nieur|dev)\b",
}
_COMPILED = {tag: re.compile(pattern, re.IGNORECASE) for tag, pattern in _RULES.items()}

_MAX_TAGS = 4


def infer_tags(text: str) -> list[str]:
    """Renvoie jusqu'à 4 tags déduits du texte, ou ['Autre'] si rien ne matche."""
    tags = [tag for tag, rx in _COMPILED.items() if rx.search(text)]
    return tags[:_MAX_TAGS] or ["Autre"]
