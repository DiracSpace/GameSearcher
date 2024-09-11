from beanie import Document
from pydantic import BaseModel
from datetime import datetime


class BaseDocument(BaseModel):
    created_by: str
    created_at: datetime
    updated_by: str
    updated_at: datetime
    deleted_by: str
    deleted_at: datetime


class BaseMongoDocument(Document, BaseDocument):
    pass
