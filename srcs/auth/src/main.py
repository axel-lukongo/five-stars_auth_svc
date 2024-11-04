
from fastapi import FastAPI
import models
# from .database import engine
# from .auth import router as auth_router
from auth import router as auth_router
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_router)
