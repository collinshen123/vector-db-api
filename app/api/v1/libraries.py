from fastapi import APIRouter, HTTPException
from app.models.library import Library
from app.repositories.library_repo import LibraryRepository

router = APIRouter()
repo = LibraryRepository()

@router.post("/", response_model=Library)
async def create_library(library: Library):
    return await repo.add_library(library)
