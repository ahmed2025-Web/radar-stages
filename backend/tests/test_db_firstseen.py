"""Tests de la base : first_seen et applied préservés entre les collectes."""
from app import db
from app.models import Offer


def _use_tmp_db(tmp_path, monkeypatch):
    dbfile = tmp_path / "radar.db"
    monkeypatch.setattr(db.config, "sqlite_path", lambda: dbfile)
    db.init_db()


def _offer(**kw) -> Offer:
    base = dict(company="X", title="T", url="u", source="linkedin", external_id="1")
    base.update(kw)
    return Offer(**base)


def test_first_seen_set_then_preserved(tmp_path, monkeypatch):
    _use_tmp_db(tmp_path, monkeypatch)
    db.upsert_offers([_offer()])
    first = db.list_offers()[0].first_seen
    assert first  # date de première détection posée

    db.upsert_offers([_offer(match=50)])  # re-collecte de la même offre
    rows = db.list_offers()
    assert len(rows) == 1                 # pas de doublon
    assert rows[0].first_seen == first    # date conservée
    assert rows[0].match == 50            # score mis à jour


def test_applied_preserved_across_upsert(tmp_path, monkeypatch):
    _use_tmp_db(tmp_path, monkeypatch)
    db.upsert_offers([_offer()])
    oid = db.list_offers()[0].id
    db.set_applied(oid, True)
    db.upsert_offers([_offer()])          # nouvelle collecte
    assert db.list_offers()[0].applied is True
