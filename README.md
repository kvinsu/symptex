# Symptex

A chatbot designed for medical students, simulating doctor-patient interactions with the goal of improving the user's medical
history-taking skills.

## Prerequisites

- [Docker](https://docs.docker.com/get-started/get-docker/)
- Browser of your choice to interact with the chatbot

## Getting Started

1. Run `docker compose up --build` in the project's root directory.
2. In another terminal, execute `docker compose exec ollama ollama pull llama3.1` to pull (download) the LLM. Depending on the internet connection as well as the model's size, this may take some time, but is only required once.
3. Interact with the Symptex chatbot locally through [Streamlit frontend URL](http://localhost:8501).

Note: The first prompt/API call usually takes a while, since the model needs to be loaded into the memory first.

## Endpoints

- Streamlit frontend: <http://localhost:8501>
- API: <http://localhost:8000>
- Ollama: <http://localhost:11434>

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
│   │   ├── symptex_chain.py      # Definition of chain
│   │   ├── prompts.py            # Definition of behavior prompts
│   │   └── patient_data.py       # Definition of patients
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
