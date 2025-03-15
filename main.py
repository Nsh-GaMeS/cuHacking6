from fastapi import FastAPI, Depends
import models 
from database import engine
from sqlalchemy.orm import Session
from routers import auth

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)