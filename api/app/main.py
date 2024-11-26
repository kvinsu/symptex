# API entry point
from dotenv import load_dotenv
from fastapi import FastAPI
from api.app.routers import chat

load_dotenv()


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
