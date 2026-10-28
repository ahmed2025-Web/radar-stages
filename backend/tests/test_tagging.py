"""Tests de l'inférence de tags."""
import pytest

from app.tagging import infer_tags


@pytest.mark.parametrize(
    "title, expected",
    [
        ("Développeur Web - Stage", "Web"),
        ("Stage - Développeur Java Microservice F/H", "Java"),
        ("AI Strategy and Governance - Stage", "IA"),          # « AI » doit matcher
        ("Software Engineer - MLOps - Stage", "DevOps"),
        ("Stage Data Scientist", "Data"),
        ("Final Year Internship Consultant - Cybersecurity", "Cybersécurité"),
        ("Stage développeur full stack", "Full-Stack"),
    ],
)
def test_infer_tags_detects_expected(title, expected):
    assert expected in infer_tags(title)


def test_ai_not_false_positive():
    # « ai » ne doit pas matcher à l'intérieur d'un mot (travail, email...).
    assert "IA" not in infer_tags("Stage travail administratif et email")


def test_infer_tags_capped_and_never_empty():
    tags = infer_tags("Développeur full stack web java python cloud IA mobile")
    assert 0 < len(tags) <= 4
    assert infer_tags("xyzzy") == ["Autre"]
