# Utiliser une image de base Python 3.11
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements dans l'image
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install iputils-ping -y
RUN ping -c 4 google.com

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le code de l'application
COPY ./src /app/src

WORKDIR /app/src

# Exposer le port sur lequel l'application s'exécute (par défaut, FastAPI utilise 8000)
EXPOSE 8000

# Démarrer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["python", "main.py"]
# CMD ["tail", "-f", "/dev/null"]
