# 📦 YouExpress API (v1.0)
**YouExpress** est une API Backend de gestion logistique pour le marché marocain. Cette version (V1) utilise une architecture **MVC** stricte, est entièrement conteneurisée avec **Docker**, et gère les acteurs logistiques (Expéditeurs, Destinataires, Livreurs, Gestionnaires) via un système d'héritage de classes.

<br>

## 🚀 Fonctionnalités Principales

- **Architecture MVC :** Séparation claire entre Modèles, Schémas, Contrôleurs et Routes.

- **Docker Ready :** Déploiement instantané via `docker-compose`.

- **Gestion des Acteurs :** CRUD distinct pour chaque type d'utilisateur (héritage de `UserBase`).

- **Workflow Colis :** Cycle de vie complet (Créé → Collecté → En Stock → En Transit → Livré).

- **Zones Géographiques :** Assignation des livreurs par zones (Villes du Maroc).

- **Traçabilité :** Historique automatique des changements d'états.

- **Logging Avancé :** Configuration centralisée des logs (`logging_conf.py`).

- **Auto-Seeding :** Peuplement automatique de la base de données au démarrage (Admin par défaut, Zones, etc.).

<br>

## 🛠️ Stack Technique

- **Langage :** Python 3.10+

- **Framework :** FastAPI

- **Base de Données :** PostgreSQL (via Docker)

- **ORM :** SQLAlchemy

- **Validation :** Pydantic

- **Infra :** Docker & Docker Compose

- **Tests :** Pytest

<br>

## 📂 Structure du Projet
L'architecture respecte une organisation modulaire :

```bash
YouExpress/
├── .env                       # Variables d'environnement (DB_URL, Secrets...)
├── .gitignore                 # Fichiers à ignorer par Git (__pycache__, .env, etc.)
├── docker-compose.yml         # Orchestration des conteneurs (App + Postgres)
├── Dockerfile                 # Image Docker de l'application Python
├── requirements.txt           # Liste des dépendances (fastapi, sqlalchemy, psycopg2...)
├── README.md                  # Documentation du projet
│
├── app/                       # Cœur de l'application
│   ├── __init__.py            # Marque le dossier comme package
│   ├── main.py                # Point d'entrée, création App, Lifespan, Health Check
│   ├── config.py              # Configuration via Pydantic (chargement du .env)
│   ├── database.py            # Configuration de la connexion DB (Session, Engine)
│   ├── exceptions.py          # Gestion centralisée des erreurs (Custom Exceptions)
│   ├── logging_conf.py        # Configuration des logs (Format, Output)
│   │
│   ├── models/                # COUCHE DONNÉES (SQLAlchemy)
│   │   ├── __init__.py        # Importe tous les models (pour le create_all)
│   │   ├── base.py            # Déclaration de la Base SQLAlchemy (declarative_base)
│   │   ├── user_base.py       # Classe abstraite 'User' (Parent des acteurs)
│   │   ├── gestionnaire.py    # Modèle Gestionnaire
│   │   ├── destinataire.py    # Modèle Destinataire
│   │   ├── expediteur.py      # Modèle Expéditeur
│   │   ├── livreur.py         # Modèle Livreur
│   │   ├── zone.py            # Modèle Zone
│   │   ├── colis.py           # Modèle Colis (avec FKs)
│   │   └── historique.py      # Modèle Historique
│   │
│   ├── schemas/               # COUCHE VALIDATION (Pydantic)
│   │   ├── __init__.py        # Exposition des schémas
│   │   ├── user_schemas.py    # Schémas pour User, Gestionnaire, Livreur, etc.
│   │   └── logistics_schemas.py # Schémas pour Zone, Colis, Historique
│   │
│   ├── controllers/           # COUCHE MÉTIER (Logique POO)
│   │   ├── __init__.py        # Exposition des contrôleurs
│   │   ├── gestionnaire_controller.py
│   │   ├── destinataire_controller.py
│   │   ├── expediteur_controller.py
│   │   ├── livreur_controller.py
│   │   ├── zone_controller.py
│   │   ├── colis_controller.py
│   │   └── historique_controller.py
│   │
│   └── routes/                # COUCHE API (Endpoints FastAPI)
│       ├── __init__.py        # Inclusion des routers
│       ├── gestionnaire_routes.py
│       ├── destinataire_routes.py
│       ├── expediteur_routes.py
│       ├── livreur_routes.py
│       ├── zone_routes.py
│       ├── colis_routes.py
│       └── historique_routes.py
│
└── tests/                     # TESTS UNITAIRES (Pytest)
    ├── __init__.py
    ├── conftest.py            # Configuration DB de test et Fixtures
    ├── test_main.py           # Test Health Check
    ├── test_users.py          # Tests des acteurs
    └── test_logistics.py      # Tests Colis et Zones
```

<br>

## ⚙️ Installation et Démarrage
### Pré-requis :

- Docker Desktop (ou Docker Engine + Compose)

- Git

### Etapes 

1. **Cloner le projet :**

```bash
git clone https://github.com/ABDELHAFIDAIT/YouExpress.git
cd YouExpress
```

2. **Configurer l'environnement** : Créez un fichier `.env` à la racine.

```js
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=youexpress_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

POSTGRES_DB_TEST=youexpress_test
POSTGRES_HOST_TEST=db
POSTGRES_PORT_TEST=5432

LOG_LEVEL=INFO
```

3. **Lancer l'application :**

```Bash
docker-compose up --build
```

Docker va télécharger l'image Postgres, construire l'image Python, et lancer le serveur.

<br>

## 📚 Documentation API

Une fois l'application lancée, la documentation interactive est disponible ici : 

👉 http://localhost:8000/docs

<br>

## 🌱 Données Initiales (Seeding)

Au démarrage de l'application (dans app/main.py), un script vérifie si la base de données est vide. Si oui, il injecte automatiquement :

- Un **Gestionnaire** Admin.

- Les **Zones** (Villes du Maroc).

- Des **Expéditeurs** et **Destinataires** de test.

- Des **Livreurs** assignés aux zones.

<br>

## 🧪 Lancer les Tests

Pour exécuter la suite de tests pytest (située dans le dossier `tests/`) :

```bash 
docker-compose exec web pytest -v
```