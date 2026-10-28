"""Score de pertinence offre ↔ profil (0–100).

Deux modes, choisis automatiquement :
  1. Embeddings (sentence-transformers) — sémantique, local, gratuit. Utilisé si
     la bibliothèque est installée.
  2. Fallback par mots-clés — recouvrement de termes techniques. Zéro dépendance,
     pour que le radar tourne partout.
"""
from __future__ import annotations

import re

from .. import config


def _tokenize(text: str) -> set[str]:
    return {t for t in re.split(r"[^a-zA-Zàâçéèêëîïôûùüÿñæœ0-9+#.]+", text.lower()) if len(t) > 1}


class Scorer:
    def __init__(self, profile_text: str):
        self.profile_text = profile_text
        self._profile_tokens = _tokenize(profile_text)
        self._model = None
        self._profile_vec = None
        self._try_load_embeddings()

    def _try_load_embeddings(self) -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._model = SentenceTransformer(config.EMBEDDING_MODEL)
            self._profile_vec = self._model.encode(self.profile_text, normalize_embeddings=True)
        except Exception:
            # Pas de sentence-transformers (ou modèle indisponible) → fallback.
            self._model = None

    @property
    def mode(self) -> str:
        return "embeddings" if self._model is not None else "keywords"

    def score(self, offer_text: str) -> int:
        if self._model is not None:
            vec = self._model.encode(offer_text, normalize_embeddings=True)
            cosine = float((self._profile_vec * vec).sum())  # vecteurs normalisés
            return max(0, min(100, round((cosine + 1) / 2 * 100)))
        return self._keyword_score(offer_text)

    def _keyword_score(self, offer_text: str) -> int:
        tokens = _tokenize(offer_text)
        if not tokens:
            return 0
        overlap = tokens & self._profile_tokens
        # Jaccard pondéré vers le recouvrement côté offre (une offre courte très
        # ciblée ne doit pas être pénalisée).
        ratio = len(overlap) / (len(tokens) ** 0.5 + 1)
        return max(0, min(100, round(ratio * 40)))
