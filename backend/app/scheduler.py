"""Relance automatique de la collecte à intervalle régulier (APScheduler).

Désactivé par défaut (SCHEDULER_ENABLED). Quand il est actif, la collecte tourne
dans un thread dédié, sans bloquer l'API.
"""
from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler

from . import config, pipeline

_scheduler: BackgroundScheduler | None = None


def start() -> BackgroundScheduler | None:
    global _scheduler
    if not config.SCHEDULER_ENABLED or _scheduler is not None:
        return _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        pipeline.run,
        trigger="interval",
        hours=config.REFRESH_INTERVAL_HOURS,
        id="refresh-offers",
        replace_existing=True,
    )
    _scheduler.start()
    return _scheduler


def stop() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
