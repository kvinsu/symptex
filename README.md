# Symptex

A chatbot designed for medical students, simulating doctor-patient interactions with the goal of improving the user's
history-taking skills.

## Prerequisites

* [Ollama](https://ollama.com/download)
* [Docker](https://docs.docker.com/get-started/get-docker/)
* Python 3.12
* Browser of your choice to interact with the chatbot

## Getting Started

1. Run `ollama serve` in a terminal window to start the ollama process (not required on Windows)
2. In another terminal window, run `ollama pull llama3.1` to pull the llama3.1 model if you haven't already
3. In the  `api/chains/` folder, create an `.env` file to define and store sensitive keys.
4. Run `docker compose up --build` in the project's root directory
5. Interact with the Symptex chatbot through the Streamlit frontend URL

Note: The first API call usually takes a while, since the model needs to be loaded into the memory first.

## Endpoints

* Streamlit frontend: <http://localhost:8501>
* API: <http://localhost:8000>
* Ollama: <http://localhost:11434>

## Project Structure

```
symptex/
│
├── api/
│   ├── app/                      # API logic
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI entry point
│   │   └── routers/
│   │       ├── __init__.py
│   │       └── chat.py           # Chat-specific routes
│   │
│   ├── chains/                   # Chain logic
│   │   ├── __init__.py
│   │   └── symptex_chain.py      # Definition of chain
│   │
│   ├── requirements.txt          # Dependencies for LangChain API
│   └── Dockerfile                # Dockerfile for LangChain API
│
├── frontend/
│   ├── frontend.py               # Streamlit frontend
│   ├── requirements.txt          # Dependencies for Streamlit frontend
│   └── Dockerfile                # Dockerfile for Streamlit frontend
│
├── docker-compose.yml            # Docker Compose to orchestrate containers
└── README.md
```
