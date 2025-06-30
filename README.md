# Vector Database From Scratch

A custom vector database implementation with embedding generation and semantic search capabilities, built from the ground up using Python, FastAPI, and Docker.

## Task Overview

This project implements a REST API for indexing and querying documents within a custom Vector Database. The system supports creating libraries, storing documents with embedded chunks, and performing k-nearest neighbor searches using vector similarity.

## Setup and Run

### Prerequisites
- Docker & Docker Compose
- Git

### Installation & Execution

```bash
# Clone the repository
git clone https://github.com/yourusername/vector-db-api
cd vector-db-api

# Create initial database file
echo "[]" > db.json

# Run with Docker (API + Frontend)
docker compose --profile ui up
```

## Architecture & Technical Choices

### Data Models
- **Chunk**: Text piece with associated 384-dimensional embedding and metadata
- **Document**: Collection of chunks with document-level metadata  
- **Library**: Collection of documents with library-level metadata

### Key Design Decisions

#### 1. Embedding Strategy
- **Choice**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Rationale**: Local model eliminates API dependencies, 384D vectors balance performance and accuracy
- **Alternative Considered**: Cohere API (rejected due to cost and external dependency)

#### 2. Vector Search Algorithms
Implemented two custom indexing algorithms (no external libraries like FAISS):

**Brute Force k-NN Search**
- **Time Complexity**: O(n·d) where n=chunks, d=embedding dimensions
- **Space Complexity**: O(n·d) 
- **Use Case**: Small datasets, guaranteed accuracy

**Centroid-Based Clustering Search**
- **Time Complexity**: O(n·d + k·c·d) where c=clusters, k=results
- **Space Complexity**: O(n·d + c·d)
- **Use Case**: Larger datasets, faster approximate search

#### 3. Data Persistence
- **Choice**: JSON file storage with volume mounting
- **Rationale**: Simple, human-readable, suitable for prototype/demo
- **Production Alternative**: PostgreSQL with pgvector extension

#### 4. Concurrency & Thread Safety
- **Current**: Single-threaded with file locking via JSON atomic writes
- **Design**: Read operations load full file, writes replace entire file atomically
- **Trade-off**: Simplicity over performance for MVP

#### 5. API Architecture
Following clean architecture principles:
- **Controllers**: FastAPI endpoints (`/api/v1/libraries.py`)
- **Services**: Business logic layer (embedded in repositories)
- **Repositories**: Data access layer (`library_repo.py`, `vector_index.py`)
- **Models**: Pydantic schemas for validation

## Features

- ✅ **Custom Vector Database Implementation**
- ✅ **RESTful API with FastAPI**
- ✅ **Automatic Embedding Generation** (Sentence Transformers)
- ✅ **Multiple Search Algorithms** (Brute force + Centroid clustering)
- ✅ **Docker Containerization** (API + UI)
- ✅ **Interactive Web Interface** (Streamlit)
- ✅ **Pydantic Schema Validation**
- ✅ **Static Type Hints Throughout**
- ✅ **SOLID Design Principles**

## API Endpoints

### Libraries
- `GET /v1/libraries/` - List all libraries
- `POST /v1/libraries/` - Create new library
- `GET /v1/libraries/{id}` - Get library by ID

### Documents & Chunks
- `POST /v1/libraries/{id}/documents` - Add document with chunks (auto-embedding)

### Search
- `POST /v1/libraries/{id}/search` - Vector search with pre-computed embedding
- `POST /v1/libraries/{id}/query` - Text search (auto-embedding)

### Access Points
- **Frontend (Streamlit UI)**: http://localhost:8501
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Project Structure

```
vector-db-api/
├── app/
│   ├── api/v1/
│   │   └── libraries.py          # FastAPI endpoints
│   ├── core/
│   │   └── embedding.py          # Sentence transformer integration
│   ├── models/
│   │   ├── chunk.py              # Pydantic models
│   │   ├── document.py
│   │   └── library.py
│   ├── repositories/
│   │   ├── library_repo.py       # Data access layer
│   │   └── vector_index.py       # Search algorithms
│   └── main.py                   # FastAPI application
├── simple_ui.py                  # Streamlit frontend
├── Dockerfile                    # API container
├── Dockerfile.streamlit          # UI container
├── docker-compose.yml            # Multi-container orchestration
├── requirements.txt              # Python dependencies
├── db.json                       # JSON persistence layer
└── README.md
```

## Technical Implementation Details

### Embedding Generation
```python
# Automatic embedding on document creation
for chunk in document.chunks:
    chunk.embedding = get_embedding(chunk.text, input_type="search_document")
```

### Vector Search Implementation
```python
# Cosine similarity calculation
def cosine_similarity(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# k-NN search with custom algorithm
def knn_search(chunks: List[Chunk], query_embedding: List[float], k: int = 5):
    scored_chunks = [
        (chunk, cosine_similarity(query_embedding, chunk.embedding))
        for chunk in chunks
    ]
    scored_chunks.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored_chunks[:k]]
```

### Error Handling & Validation
- Pydantic automatic request/response validation
- HTTP status code constants (no hardcoded values)
- Graceful degradation for missing dependencies
- Dimension mismatch detection and filtering

## Dependencies

### Core Runtime
- `fastapi==0.104.1` - REST API framework
- `sentence-transformers==2.2.2` - Embedding generation
- `pydantic==2.5.0` - Data validation
- `numpy==1.24.3` - Vector operations
- `uvicorn==0.24.0` - ASGI server

### Development & UI
- `streamlit==1.28.0` - Web interface
- `requests==2.31.0` - HTTP client