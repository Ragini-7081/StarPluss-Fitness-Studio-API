
import threading
import webbrowser

from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routes import router
from app.logging_config import logger

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StarPluss Fitness Studio API",
    description="API for user authentication, fitness classes, and bookings.",
    version="1.0.0",
)

app.include_router(router)


@app.on_event("startup")
def open_docs_automatically():
    threading.Timer(
        1.5,
        lambda: webbrowser.open("http://127.0.0.1:8000/docs"),
    ).start()


@app.get("/")
def home():
    return {
        "message": "Welcome to StarPluss Fitness Studio API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
