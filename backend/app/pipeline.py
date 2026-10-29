"""Pipeline : collecte → dédoublonnage → scoring → stockage."""
from __future__ import annotations

from . import config, db
from .collectors import COLLECTORS
from .matching import Scorer
from .models import Offer


def run(sources: list[str] | None = None) -> dict:
    """Lance la collecte sur les sources demandées (ACTIVE_COLLECTORS par défaut).

    Résilient : si une source échoue (réseau, blocage, HTML changé), on la saute
    et on continue avec les autres."""
    sources = sources or config.ACTIVE_COLLECTORS

    collected: dict[str, Offer] = {}
    errors: dict[str, str] = {}
    for name in sources:
        collector = COLLECTORS.get(name)
        if collector is None:
            continue
        try:
            source_offers = collector()
        except Exception as exc:  # une source défaillante ne casse pas le pipeline
            errors[name] = str(exc)
            continue
        for offer in source_offers:
            collected[offer.id] = offer  # la clé dédoublonne

    offers = list(collected.values())

    scorer = Scorer(config.read_profile())
    for offer in offers:
        offer.match = scorer.score(offer.match_text())

    offers.sort(key=lambda o: o.match, reverse=True)
    db.init_db()
    db.upsert_offers(offers)

    return {
        "collected": len(offers),
        "sources": sources,
        "scoring": scorer.mode,
        "errors": errors,
    }


if __name__ == "__main__":
    print(run())
