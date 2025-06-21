from fastapi import APIRouter, HTTPException
from app.models.library import Library
from app.repositories.library_repo import LibraryRepository
from app.models.document import Document
from app.models.chunk import Chunk
from app.repositories.vector_index import knn_search , centroid_based_search
from typing import List
from pydantic import BaseModel



router = APIRouter()
repo = LibraryRepository()

# create a new library
@router.post("/", response_model=Library)
async def create_library(library: Library):
    return await repo.add_library(library)

# appending a document to an existing library
@router.post("/{library_id}/documents", response_model=Library)
async def add_document(library_id: str, document: Document):
    updated_library = await repo.add_document_to_library(library_id, document)
    if not updated_library:
        raise HTTPException(status_code=404, detail="Library not found")
    return updated_library

# retrieving a library by its ID
@router.get("/{library_id}", response_model=Library)
async def get_library(library_id: str):
    library = await repo.get_library(library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")
    return library

# listing all libraries
@router.get("/", response_model=list[Library])
async def list_libraries():
    return await repo.list_libraries()


class SearchRequest(BaseModel):
    embedding: List[float]
    k: int = 5
    method: str = "centroid"  # or "brute"


@router.post("/{library_id}/search", response_model=List[Chunk])
async def search_chunks(library_id: str, request: SearchRequest):
    library = await repo.get_library(library_id)
    if not library:
        raise HTTPException(status_code=404, detail="Library not found")

    all_chunks = [chunk for doc in library.documents for chunk in doc.chunks]
    if not all_chunks:
        raise HTTPException(status_code=400, detail="No chunks to search")

    if request.method == "centroid":
        return centroid_based_search(all_chunks, request.embedding, k=request.k)
    else:
        return knn_search(all_chunks, request.embedding, k=request.k)

