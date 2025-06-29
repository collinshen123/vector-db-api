from fastapi import FastAPI
from app.api.v1 import libraries
import os

app = FastAPI(
    title="Vector Database API",
    description="A custom vector database with semantic search capabilities",
    version="1.0.0"
)

app.include_router(libraries.router, prefix="/v1/libraries", tags=["libraries"])

@app.get("/")
def read_root():
    return {
        "message": "Vector DB API is running!", 
        "docs": "/docs",
        "endpoints": {
            "libraries": "/v1/libraries/",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "vector-db-api"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
