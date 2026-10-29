# Image de déploiement autonome : embarque le backend, le frontend et le profil,
# pour tourner telle quelle sur une plateforme (Render, Railway, Fly, k8s…).
FROM python:3.12-slim

WORKDIR /app

# Dépendances d'abord (cache Docker).
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Code + ressources servies au runtime.
COPY backend/app backend/app
COPY frontend frontend
COPY profile profile

# La plateforme fournit souvent le port via $PORT.
ENV PORT=8000
EXPOSE 8000

# --app-dir backend : rend le package "app" importable ; la racine du projet
# reste /app, donc frontend/ et profile/ sont trouvés comme en local.
CMD ["sh", "-c", "uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port ${PORT:-8000}"]
