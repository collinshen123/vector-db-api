from fastapi import APIRouter, HTTPException
from app.models.library import Library
from app.repositories.library_repo import LibraryRepository
from app.models.document import Document


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