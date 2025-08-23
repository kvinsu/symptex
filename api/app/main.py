# API entry point
from fastapi import FastAPI
from app.routers import chat
from app.db.db import engine
from app.db import models

app = FastAPI(
    title="Symptex LangChain Server",
    version="1.0",
    description="API server for Symptex, a LangChain-based chat application for patient simulation",
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Include chat router
app.include_router(chat.router, prefix="/api/v1")

# Init database schema
models.Base.metadata.create_all(bind=engine)
