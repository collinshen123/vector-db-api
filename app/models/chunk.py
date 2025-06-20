from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timezone

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    embedding: List[float]
    metadata: Optional[dict] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
