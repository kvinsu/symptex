# Base image
FROM python:3.12-slim

WORKDIR /symptex

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ./api

ENV PYTHONPATH=/symptex

CMD ["uvicorn", "api.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]
