"""Tests de fumée : le pipeline collecte et l'API sert des offres valides."""
from fastapi.testclient import TestClient

from app import pipeline
from app.main import app


def test_pipeline_collects_and_scores():
    res = pipeline.run()
    assert res["collected"] > 0
    assert res["scoring"] in {"embeddings", "keywords"}


def test_offers_endpoint():
    with TestClient(app) as client:
        resp = client.get("/api/offers")
        assert resp.status_code == 200
        offers = resp.json()
        assert len(offers) > 0
        for offer in offers:
            assert {"company", "title", "url", "match"} <= offer.keys()
            assert 0 <= offer["match"] <= 100


def test_offers_sorted_by_match_desc():
    with TestClient(app) as client:
        offers = client.get("/api/offers").json()
    scores = [o["match"] for o in offers]
    assert scores == sorted(scores, reverse=True)
