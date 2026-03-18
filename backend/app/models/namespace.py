from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class AppNamespace(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    prefix: str = Field(unique=True, index=True)
    uri: str = Field(unique=True)
