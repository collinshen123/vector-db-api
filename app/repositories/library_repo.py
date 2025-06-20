from app.models.library import Library
import asyncio
from app.models.document import Document


class LibraryRepository:
    def __init__(self):
        self._libraries = {}
        self._lock = asyncio.Lock()

    async def add_library(self, library: Library) -> Library:
        async with self._lock:
            self._libraries[library.id] = library
            return library
        
    async def add_document_to_library(self, library_id: str, document: Document) -> Library | None:
        async with self._lock:
            library = self._libraries.get(library_id)
            if not library:
                return None
            library.documents.append(document)
            return library

    async def get_library(self, library_id: str) -> Library | None:
        async with self._lock:
            return self._libraries.get(library_id)

    async def list_libraries(self) -> list[Library]:
        async with self._lock:
            return list(self._libraries.values())

    async def delete_library(self, library_id: str) -> bool:
        async with self._lock:
            return self._libraries.pop(library_id, None) is not None
