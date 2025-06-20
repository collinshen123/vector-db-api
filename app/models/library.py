from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone
from .document import Document

class Library(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    documents: List[Document] = []
    metadata: Optional[dict] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
