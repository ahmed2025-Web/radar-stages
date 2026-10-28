"""Pipeline : collecte → dédoublonnage → scoring → stockage."""
from __future__ import annotations

from . import config, db
from .collectors import COLLECTORS
from .matching import Scorer
from .models import Offer


def _load_profile() -> str:
    try:
        return config.PROFILE_PATH.read_text(encoding="utf-8")
    except OSError:
        return ""


def run(sources: list[str] | None = None) -> dict:
    """Lance la collecte sur les sources demandées (toutes par défaut) et met à jour la base."""
    sources = sources or list(COLLECTORS)

    collected: dict[str, Offer] = {}
    for name in sources:
        collector = COLLECTORS.get(name)
        if collector is None:
            continue
        for offer in collector():
            collected[offer.id] = offer  # la clé dédoublonne

    offers = list(collected.values())

    scorer = Scorer(_load_profile())
    for offer in offers:
        offer.match = scorer.score(offer.match_text())

    offers.sort(key=lambda o: o.match, reverse=True)
    db.init_db()
    db.upsert_offers(offers)

    return {"collected": len(offers), "sources": sources, "scoring": scorer.mode}


if __name__ == "__main__":
    print(run())
