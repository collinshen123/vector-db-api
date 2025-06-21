from app.models.library import Library
import asyncio
from app.models.document import Document
import json
import os
from app.models.library import Library
from pydantic.json import pydantic_encoder



class LibraryRepository:
    def __init__(self, db_path: str = "db.json"):
        self._libraries = {}
        self._lock = asyncio.Lock()
        self.db_path = db_path
        self._load_from_disk()

    def _load_from_disk(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                raw_data = json.load(f)
                self._libraries = {
                    lib["id"]: Library(**lib) for lib in raw_data
                }

    def _save_to_disk(self):
        with open(self.db_path, "w") as f:
            json.dump(list(self._libraries.values()), f, default=pydantic_encoder, indent=2)

    async def add_library(self, library: Library) -> Library:
        async with self._lock:
            self._libraries[library.id] = library
            self._save_to_disk()
            return library

    async def get_library(self, library_id: str) -> Library | None:
        async with self._lock:
            return self._libraries.get(library_id)

    async def list_libraries(self) -> list[Library]:
        async with self._lock:
            return list(self._libraries.values())

    async def delete_library(self, library_id: str) -> bool:
        async with self._lock:
            removed = self._libraries.pop(library_id, None)
            self._save_to_disk()
            return removed is not None

    async def add_document_to_library(self, library_id: str, document) -> Library | None:
        async with self._lock:
            library = self._libraries.get(library_id)
            if not library:
                return None
            library.documents.append(document)
            self._save_to_disk()
            return library

