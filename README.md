# Vector Database From Scratch

A custom vector database with embedding generation and semantic search using sentence transformers and FastAPI.

## Setup and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/vector-db-api
cd vector-db-api

# Create initial database file
echo "[]" > db.json

# Run with Docker (API + Frontend)
docker compose --profile ui up
```

## Access

- Frontend (Streamlit UI): http://localhost:8501
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Endpoints

- `POST /v1/libraries/` - Create library
- `POST /v1/libraries/{id}/documents` - Add document with chunks
- `POST /v1/libraries/{id}/search` - Search with embedding vector
- `POST /v1/libraries/{id}/query` - Search with text query

## Features

- Custom vector database implementation
- Sentence transformer embeddings (384 dimensions)
- Cosine similarity and centroid-based search
- JSON file persistence
- RESTful API with FastAPI
- Interactive web interface with Streamlit
