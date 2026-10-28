"""Stockage des offres. SQLite via la bibliothèque standard (zéro dépendance).

Migration vers PostgreSQL : remplacer cette couche par SQLAlchemy/SQLModel sans
toucher au reste (le pipeline ne connaît que upsert_offers / list_offers)."""
from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager

from . import config
from .models import Offer


@contextmanager
def _conn():
    path = config.sqlite_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


def init_db() -> None:
    with _conn() as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS offers (
                id       TEXT PRIMARY KEY,
                match    INTEGER DEFAULT 0,
                applied  INTEGER DEFAULT 0,
                data     TEXT NOT NULL
            )
            """
        )


def upsert_offers(offers: list[Offer]) -> int:
    """Insère ou met à jour les offres. Préserve le flag `applied` déjà en base."""
    with _conn() as con:
        known_applied = {
            row["id"] for row in con.execute("SELECT id FROM offers WHERE applied = 1")
        }
        for o in offers:
            if o.id in known_applied:
                o.applied = True
            con.execute(
                "INSERT INTO offers (id, match, applied, data) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET match=excluded.match, data=excluded.data",
                (o.id, o.match, int(o.applied), o.model_dump_json()),
            )
    return len(offers)


def list_offers() -> list[Offer]:
    with _conn() as con:
        rows = con.execute("SELECT data FROM offers ORDER BY match DESC").fetchall()
    return [Offer(**json.loads(r["data"])) for r in rows]


def set_applied(offer_id: str, applied: bool = True) -> None:
    with _conn() as con:
        con.execute(
            "UPDATE offers SET applied = ? WHERE id = ?", (int(applied), offer_id)
        )
