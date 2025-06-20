from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from .chunk import Chunk

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    chunks: List[Chunk] = []
    metadata: Optional[dict] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
