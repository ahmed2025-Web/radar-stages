"""API FastAPI : sert les offres (JSON) et le frontend radar."""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from . import config, db, pipeline


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    # Premier remplissage si la base est vide (offres de démo).
    if not db.list_offers():
        pipeline.run()
    yield


app = FastAPI(title="Radar Stages", version="0.1.0", lifespan=lifespan)


@app.get("/api/offers")
def get_offers():
    offers = db.list_offers()
    return JSONResponse([o.model_dump() | {"id": o.id} for o in offers])


@app.post("/api/refresh")
def refresh(sources: list[str] | None = None):
    """Relance la collecte et le scoring."""
    return pipeline.run(sources)


@app.post("/api/offers/{offer_id}/applied")
def mark_applied(offer_id: str, applied: bool = True):
    if not any(o.id == offer_id for o in db.list_offers()):
        raise HTTPException(404, "Offre inconnue")
    db.set_applied(offer_id, applied)
    return {"id": offer_id, "applied": applied}


@app.get("/")
def index():
    idx = config.FRONTEND_DIR / "index.html"
    if not idx.exists():
        return JSONResponse({"error": "frontend/index.html introuvable"}, status_code=404)
    return FileResponse(idx)
