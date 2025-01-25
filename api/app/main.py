# API entry point
from fastapi import FastAPI
from api.app.routers import chat


app = FastAPI(
    title="Symptex LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Include chat router
app.include_router(chat.router, prefix="/api/v1")
