"""Tests du parseur LinkedIn — sur une fixture HTML, sans appel réseau."""
from pathlib import Path

from app.collectors.linkedin import parse_jobs

FIXTURE = Path(__file__).parent / "fixtures" / "linkedin_sample.html"


def test_parse_jobs_extracts_offers():
    offers = parse_jobs(FIXTURE.read_text(encoding="utf-8"))
    assert len(offers) == 2

    first = offers[0]
    assert first.company == "Dassault Systèmes"
    assert first.title == "Stage – Ingénieur Développement IA"
    assert first.source == "linkedin"
    assert first.location == "Paris, Île-de-France, France"
    assert first.posted == "il y a 1 semaine"
    # L'URL est nettoyée des paramètres de tracking.
    assert first.url == "https://www.linkedin.com/jobs/view/4482138321/"
    # L'id LinkedIn est extrait de l'URL et sert d'identité stable.
    assert first.external_id == "4482138321"
    assert first.id == "linkedin:4482138321"
    # Les tags sont inférés depuis l'intitulé.
    assert "IA" in first.tags


def test_parse_jobs_dedup_key_uses_linkedin_id():
    offers = parse_jobs(FIXTURE.read_text(encoding="utf-8"))
    # Deux annonces distinctes -> deux ids distincts.
    assert offers[0].id != offers[1].id
    # Même id LinkedIn -> même identité (dédoublonnage fiable).
    offers[1].external_id = offers[0].external_id
    assert offers[1].id == offers[0].id


def test_parse_jobs_infers_tags():
    offers = parse_jobs(FIXTURE.read_text(encoding="utf-8"))
    second = offers[1]  # "Software Engineer Data"
    assert "Data" in second.tags
    assert "Dev" in second.tags


def test_parse_jobs_skips_malformed_cards():
    assert parse_jobs("<ul><li>pas une offre</li></ul>") == []
