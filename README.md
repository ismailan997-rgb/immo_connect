# Immo Connect

Plateforme immobilière Flask pour publier et rechercher des biens au Sénégal.

## Prérequis

- Python 3.11 ou supérieur
- Une base PostgreSQL accessible

## Installation locale sous Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Renseignez `DATABASE_URL` et `IMMO_CONNECT_SECRET_KEY` dans `.env`, puis lancez :

```powershell
py app.py
```

L'application crée les tables PostgreSQL au démarrage. L'URL PostgreSQL doit être correctement encodée si le mot de passe contient des caractères spéciaux.

## Migrer la base SQLite existante

Faites d'abord une copie de sauvegarde de `database.db`. Configurez `DATABASE_URL` vers une base PostgreSQL vide, puis exécutez :

```powershell
py migrate_sqlite_to_postgres.py
```

Le script copie les utilisateurs, annonces et avis en conservant leurs identifiants. Il refuse de démarrer si les tables PostgreSQL contiennent déjà des données.

## Production

Définissez `DATABASE_URL` et une valeur stable et aléatoire pour `IMMO_CONNECT_SECRET_KEY` dans les variables d'environnement de l'hébergeur. Lancez l'application avec Gunicorn, par exemple `gunicorn --bind 0.0.0.0:$PORT app:app` sur un hébergement Linux.

Les photos sont encore stockées dans `static/uploads` sur le serveur. Pour une production sans disque persistant, configurez un stockage de fichiers durable avant d'accepter des annonces réelles.