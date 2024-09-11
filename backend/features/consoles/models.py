from backend.core.base_model import BaseMongoDocument


class ConsoleDocument(BaseMongoDocument):
    name: str

    class Settings:
        name = "consoles"
