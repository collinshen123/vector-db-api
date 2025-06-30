# Vector Database From Scratch

A custom vector database with embedding generation and semantic search using sentence transformers and FastAPI.

## Setup and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/vector-db-api
cd vector-db-api

# Create initial database file
echo "[]" > db.json

# Build and run with Docker
docker build -t vector-db-api .
docker run -p 8000:8000 -v $(pwd)/db.json:/app/db.json vector-db-api
```

## Access

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
