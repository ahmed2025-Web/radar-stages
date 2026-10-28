"""Génération de texte via LLM (interface pluggable)."""
from .base import LLMClient, get_llm

__all__ = ["LLMClient", "get_llm"]
