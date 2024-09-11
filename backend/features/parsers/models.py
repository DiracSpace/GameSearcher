from backend.core.base_model import BaseMongoDocument


class ParserDocument(BaseMongoDocument):
    name: str
    script: str
