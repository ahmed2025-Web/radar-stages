"""Interface LLM commune. Brancher un nouveau fournisseur = une sous-classe.

Volontairement découplé : le reste du code appelle get_llm().generate(...) sans
savoir si c'est Mistral, Ollama ou autre.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .. import config


class LLMClient(ABC):
    @abstractmethod
    def available(self) -> bool:
        """True si le client est utilisable (clé présente, serveur joignable…)."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        ...


class DisabledLLM(LLMClient):
    """Mode dégradé : aucune génération. Le radar reste fonctionnel."""

    def available(self) -> bool:
        return False

    def generate(self, prompt: str) -> str:
        return "(Génération de texte désactivée — renseigne MISTRAL_API_KEY dans .env)"


def get_llm() -> LLMClient:
    if config.LLM_PROVIDER == "mistral" and config.MISTRAL_API_KEY:
        from .mistral import MistralLLM

        return MistralLLM()
    return DisabledLLM()
