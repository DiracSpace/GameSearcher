from beanie import Link
from backend.core.base_model import BaseMongoDocument
from backend.features.parsers.models import ParserDocument
from pydantic import Field, HttpUrl
from uuid import UUID, uuid4


class SourceDocument(BaseMongoDocument):
    id: UUID = Field(default_factory=uuid4)  # type: ignore
    name: str
    url: HttpUrl
    parserId: Link[ParserDocument]

    class Settings:
        name = "sources"
        validate_on_save = True
