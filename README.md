# Radar Stages 🛰️

Un agrégateur d'offres de stage qui va chercher les annonces sur plusieurs sites,
calcule un **score de pertinence par IA** entre chaque offre et mon CV, et les
affiche dans une interface type job board — triées par match, avec un lien direct
pour postuler.

Projet construit pendant ma recherche de stage de fin d'études (dev logiciel & IA).

## Pourquoi

Chercher un stage, c'est répéter les mêmes recherches sur LinkedIn, Welcome to the
Jungle, JobTeaser… et trier à la main des dizaines d'offres dont la moitié ne
correspond pas. Le radar fait ce travail : il **collecte**, **dédoublonne**,
**score** et **présente**.

## Architecture

```
Collecteurs ─▶ Pipeline ─▶ Matching IA ─▶ Base ─▶ API ─▶ Frontend
(LinkedIn,      (dédup +     (embeddings    (SQLite/  (FastAPI) (job board)
 WTTJ, …)        scoring)     vs CV)         Postgres)
```

- **Collecteurs** (`backend/app/collectors/`) : un adaptateur par source. Chacun
  renvoie une liste d'`Offer` normalisées. `sample` fournit des offres réelles de
  démo pour que l'app tourne sans scraper.
- **Matching** (`backend/app/matching/`) : score de pertinence offre ↔ profil.
  Utilise `sentence-transformers` (embeddings, local et gratuit) si installé,
  sinon un scorer par recouvrement de mots-clés — l'app marche dans les deux cas.
- **LLM** (`backend/app/llm/`) : interface pluggable pour la génération de texte
  (résumé d'offre, brouillon de lettre). Implémentation Mistral (tier gratuit) ;
  on peut brancher Ollama / autre sans toucher au reste.
- **API** (`backend/app/main.py`) : FastAPI, sert les offres et le frontend.
- **Frontend** (`frontend/index.html`) : l'interface radar (cartes, filtres pays /
  remote / techno, score, bouton « Voir l'offre »).

## Stack

Python 3.12 · FastAPI · SQLite (→ PostgreSQL) · sentence-transformers · Mistral API
· Docker · frontend HTML/JS (migration React possible).

## Démarrage rapide

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env     # puis renseigne MISTRAL_API_KEY (optionnel)
uvicorn app.main:app --reload
```

Puis ouvre http://localhost:8000 — le frontend s'affiche avec les offres de démo.

Avec Docker :

```bash
docker compose up --build
```

## Configuration

Voir `.env.example`. Tout est optionnel pour un premier run : sans clé Mistral et
sans `sentence-transformers`, le radar fonctionne en mode dégradé (scoring par
mots-clés, pas de génération de texte).

## Feuille de route

- [x] Modèle d'offre + base + API + frontend
- [x] Scoring avec fallback mots-clés
- [x] Interface radar (filtres, score, lien postuler)
- [x] Collecteur LinkedIn (API publique « guest », scraping respectueux)
- [ ] Collecteurs Welcome to the Jungle & JobTeaser
- [ ] Filtre pays (France + international)
- [ ] Scoring par embeddings branché sur le CV réel
- [x] Génération de brouillon de lettre via LLM (Mistral)
- [x] Scheduler quotidien + nouveautés mises en évidence
- [x] Déploiement (image Docker autonome + blueprint Render)

## Déploiement

Le projet se déploie via une **image Docker autonome** (elle embarque le backend,
le frontend et le profil).

En local :

```bash
docker compose up --build        # radar sur http://localhost:8000
```

Sur **Render** (gratuit, depuis GitHub) :
1. New + → **Blueprint** → connecte ce repo (il lit `render.yaml`).
2. Renseigne `MISTRAL_API_KEY` dans le dashboard (optionnel, pour les lettres).
3. Apply → Render build l'image et fournit une URL `…onrender.com`.

Variables utiles : `ACTIVE_COLLECTORS` (`linkedin` pour de vraies offres, `sample`
si l'IP cloud est bloquée), `SCHEDULER_ENABLED`, `REFRESH_INTERVAL_HOURS`.

> L'image reste légère : le scoring tourne en mode mots-clés (sentence-transformers
> n'est pas embarqué, trop lourd pour un tier gratuit).

## Licence

MIT — voir [LICENSE](LICENSE).
