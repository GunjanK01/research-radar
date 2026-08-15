FROM python:3.11-slim

WORKDIR /app

# System deps needed for psycopg2 build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bake the sentence-transformers model into the image at BUILD time, not first-request
# time. This is deliberate: the evaluator's `docker compose up` should never need
# internet access at runtime to download model weights. See DECISIONS_LOG D003.
ENV EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
