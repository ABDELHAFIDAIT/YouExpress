# Utiliser une image Python légère officielle
FROM python:3.10-slim

# Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# Empêcher Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# Forcer l'affichage des logs en temps réel
ENV PYTHONUNBUFFERED 1

# Copier le fichier de dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet
COPY . .

# Commande de démarrage par défaut (mode reload activé pour le développement)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]