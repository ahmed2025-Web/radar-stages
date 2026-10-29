"""Tests de la génération de lettre — sans appel réseau (LLM injecté / mocké)."""
from fastapi.testclient import TestClient

from app import letters, main
from app.llm.base import LLMClient
from app.models import Offer

OFFER = Offer(
    company="Theodo",
    title="Software Engineer Fullstack - Stage",
    url="https://example.test/offre",
    source="linkedin",
    external_id="123",
    tags=["Full-Stack", "Dev"],
    description="Stack React et Node.",
)
PROFILE = "Étudiant à Polytech Montpellier. Expérience Node, React et Python."


class FakeLLM(LLMClient):
    def available(self) -> bool:
        return True

    def generate(self, prompt: str) -> str:
        return "LETTRE GENEREE"


def test_build_prompt_contains_offer_and_profile():
    prompt = letters.build_prompt(OFFER, PROFILE)
    assert "Theodo" in prompt
    assert "Software Engineer Fullstack" in prompt
    assert "Node" in prompt                 # vient du profil
    assert "invente" in prompt.lower()       # consigne anti-invention présente


def test_generate_uses_injected_llm():
    assert letters.generate_cover_letter(OFFER, PROFILE, FakeLLM()) == "LETTRE GENEREE"


def test_letter_endpoint_404_for_unknown_offer():
    with TestClient(main.app) as client:
        resp = client.post("/api/offers/inconnu/letter")
    assert resp.status_code == 404


def test_letter_endpoint_returns_letter(monkeypatch):
    monkeypatch.setattr(main, "get_llm", FakeLLM)
    with TestClient(main.app) as client:
        offer_id = client.get("/api/offers").json()[0]["id"]
        resp = client.post(f"/api/offers/{offer_id}/letter")
    assert resp.status_code == 200
    assert resp.json()["letter"] == "LETTRE GENEREE"
