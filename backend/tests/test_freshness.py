"""Tests de la détection des offres « nouvelles »."""
from datetime import datetime, timedelta, timezone

from app import freshness


def test_is_new_for_recent():
    assert freshness.is_new(freshness.now_iso(), 24) is True


def test_not_new_when_too_old():
    old = (datetime.now(timezone.utc) - timedelta(hours=48)).isoformat()
    assert freshness.is_new(old, 24) is False


def test_not_new_for_empty_or_invalid():
    assert freshness.is_new("", 24) is False
    assert freshness.is_new("pas une date", 24) is False
