import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Si la variable d'environnement n'existe pas, on met l'URL locale par défaut
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Récupérer les variables d'environnement
API_URL = os.getenv("API_URL")

DATABASE_HOST = os.getenv("DATABASE_HOST")

DATABASE_PORT = os.getenv("DATABASE_PORT")

DATABASE_USER = os.getenv("DATABASE_USER")

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

DATABASE_NAME = os.getenv("DATABASE_NAME")