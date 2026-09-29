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

Renseignez `DATABASE_URL`, `IMMO_CONNECT_SECRET_KEY` et les variables Cloudinary de `.env.example` dans `.env`, puis lancez :

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

## Images durables avec Cloudinary

Créez un compte Cloudinary et renseignez `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY` et `CLOUDINARY_API_SECRET` dans `.env` et dans les variables d'environnement de Render. Les nouvelles photos seront envoyées dans le dossier `immo-connect/properties` ; leur URL sécurisée sera enregistrée dans PostgreSQL.

Après avoir configuré Cloudinary, transférez les photos locales encore présentes :

```powershell
py migrate_images_to_cloudinary.py
```

Le script ignore les images déjà hébergées sur Cloudinary ou les fichiers locaux absents. Conservez une sauvegarde de `database.db` et de `static/uploads` jusqu'à vérification du transfert.

## Production

Définissez `DATABASE_URL` et une valeur stable et aléatoire pour `IMMO_CONNECT_SECRET_KEY` dans les variables d'environnement de l'hébergeur. Lancez l'application avec Gunicorn, par exemple `gunicorn --bind 0.0.0.0:$PORT app:app` sur un hébergement Linux.

Sans identifiants Cloudinary configurés, les photos sont stockées localement dans `static/uploads`. En production, configurez Cloudinary avant d'accepter des annonces réelles.