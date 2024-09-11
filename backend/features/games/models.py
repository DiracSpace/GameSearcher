from typing import List, Optional
from backend.core.base_model import BaseMongoDocument
from beanie import Link
from backend.features.consoles.models import ConsoleDocument
from backend.features.sources.models import SourceDocument


class GameDocument(BaseMongoDocument):
    title: str
    description: Optional[str] = None
    consoleId: Link[ConsoleDocument]
    sourceIds: List[SourceDocument]

    class Settings:
        name = "games"
