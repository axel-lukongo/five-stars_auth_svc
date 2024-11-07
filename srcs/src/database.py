from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "postgresql://auth_db:authpsw@localhost:5432/postgre_auth"  # Change avec tes infos


url = os.getenv("DATABASE_URL")

if url:
    SQLALCHEMY_DATABASE_URL = "postgresql://auth_db:authpsw@localhost:5432/postgre_auth"
else:
    SQLALCHEMY_DATABASE_URL = "postgresql://auth_db:authpsw@postgres-service:5432/postgre_auth"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
