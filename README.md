# Symptex

## Getting Started

1. Run `ollama serve` to start the ollama application
2. In another terminal window, run `ollama pull llama3` to pull the llama3 model if you haven't already
3. Run `docker compose up --build` in the project's root directory
4. Interact with Symptex through the Streamlit frontend URL

## Endpoints

* API: http://localhost:8000
* Streamlit frontend: http://localhost:8501
* Ollama: http://localhost:11434

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

