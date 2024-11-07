from fastapi.testclient import TestClient
from main import app  # Assurez-vous que c'est le bon chemin d'importation pour votre FastAPI app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, SessionLocal
import crud, schemas

# Crée une base de données en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "postgresql://auth_db:authpsw@localhost:5432/postgre_auth"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée les tables dans la base de données en mémoire
Base.metadata.create_all(bind=engine)

# Test client FastAPI
client = TestClient(app)

# Utilitaire pour obtenir une session de base de données de test
def get_db_test():
    db = SessionLocalTest()
    try:
        yield db
    finally:
        db.close()

# Test pour l'enregistrement d'un utilisateur
def test_register():
    # Données d'utilisateur pour l'enregistrement
    user_data = {
        "username": "testuser0",
        "password": "testpassword"
    }

    # Enregistrer un utilisateur
    response = client.post("/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["username"] == user_data["username"]

    # Vérifier que l'utilisateur est bien enregistré dans la base de données
    db = next(get_db_test())
    db_user = crud.get_user(db, username=user_data["username"])
    assert db_user is not None
    assert db_user.username == user_data["username"]

# Test pour la connexion d'un utilisateur
def test_login():
    # Données d'utilisateur pour l'enregistrement
    user_data = {
        "username": "testuser1",
        "password": "testpassword"
    }

    # Créer un utilisateur dans la base de données
    db = next(get_db_test())
    user_create = schemas.UserCreate(**user_data)
    crud.create_user(db=db, user_create=user_create)

    # Essayer de se connecter avec les mêmes données
    response = client.post("/login", json=user_data)
    assert response.status_code == 200
    assert "token" in response.json()  # Vérifier que le token est dans la réponse

    # Vérifier que le token renvoyé contient l'ID de l'utilisateur
    token = response.json()["token"]
    assert token is not None



# Test de l'échec de la connexion avec un mot de passe incorrect
def test_login_fail_wrong_password():
    user_data = {
        "username": "testuser0",
        "password": "wrongpassword"
    }

    # Essayer de se connecter avec des mauvais identifiants
    response = client.post("/login", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
