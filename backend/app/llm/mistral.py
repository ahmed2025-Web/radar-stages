"""Implémentation Mistral (tier gratuit). Utilisée seulement si MISTRAL_API_KEY est défini."""
from __future__ import annotations

import time

import httpx

from .. import config
from .base import LLMClient

_ENDPOINT = "https://api.mistral.ai/v1/chat/completions"


class MistralLLM(LLMClient):
    def available(self) -> bool:
        return bool(config.MISTRAL_API_KEY)

    def generate(self, prompt: str) -> str:
        # Un retry en cas de 429 (limite de débit souvent transitoire).
        for attempt in range(2):
            resp = httpx.post(
                _ENDPOINT,
                headers={"Authorization": f"Bearer {config.MISTRAL_API_KEY}"},
                json={
                    "model": config.MISTRAL_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.4,
                },
                timeout=30,
            )
            if resp.status_code == 429 and attempt == 0:
                time.sleep(2)
                continue
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"].strip()
        resp.raise_for_status()  # 429 persistant : on laisse remonter l'erreur
        return ""
