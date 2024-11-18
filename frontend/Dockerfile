# frontend/Dockerfile
FROM python:3.12-slim

WORKDIR /symptex/frontend

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY frontend.py frontend.py

CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--logger.level=debug"]
