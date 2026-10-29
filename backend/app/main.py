"""API FastAPI : sert les offres (JSON) et le frontend radar."""
from __future__ import annotations

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from . import config, db, letters, pipeline
from .llm import get_llm


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


@app.post("/api/offers/{offer_id}/letter")
def cover_letter(offer_id: str):
    """Génère un brouillon de lettre de motivation adapté à l'offre."""
    offer = next((o for o in db.list_offers() if o.id == offer_id), None)
    if offer is None:
        raise HTTPException(404, "Offre inconnue")
    llm = get_llm()
    if not llm.available():
        raise HTTPException(503, "Génération désactivée : renseigne MISTRAL_API_KEY dans .env")
    try:
        letter = letters.generate_cover_letter(offer, config.read_profile(), llm)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 429:
            raise HTTPException(503, "Limite d'API Mistral atteinte — réessaie dans un instant.") from exc
        raise HTTPException(502, "Le service de génération a renvoyé une erreur.") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(502, "Service de génération injoignable.") from exc
    return {"offer_id": offer_id, "letter": letter}


@app.get("/")
def index():
    idx = config.FRONTEND_DIR / "index.html"
    if not idx.exists():
        return JSONResponse({"error": "frontend/index.html introuvable"}, status_code=404)
    return FileResponse(idx)
