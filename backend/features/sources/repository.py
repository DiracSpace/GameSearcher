from typing import List
from uuid import UUID
from backend.core.base_repository import BaseRepository
from backend.core.find_query import FindQuery
from backend.features.sources.models import SourceDocument
from beanie.exceptions import DocumentNotFound


class SourcesRepository(BaseRepository[SourceDocument]):
    async def get_all(self, query: FindQuery) -> List[SourceDocument]:
        return (
            await SourceDocument.find(filter=query.filter)
            .skip(query.skip)
            .limit(query.limit)
            .to_list()
        )

    async def get_by_id(self, id: UUID) -> SourceDocument:
        document = await SourceDocument.get(id)

        if document is None:
            raise DocumentNotFound(f"Could not find {SourceDocument.name} with ID={id}")

        return document

    async def get_by_id_or_default(self, id: UUID) -> SourceDocument | None:
        return await SourceDocument.get(id)

    async def create(self, model: SourceDocument) -> UUID:
        createdDocument = await SourceDocument.create(model)
        return createdDocument.id

    async def update(self, model: SourceDocument):
        document = await self.get_by_id(model.id)
        await document.update(model)
        await document.save()

    async def delete(self, id: UUID):
        document = await self.get_by_id(id)
        await document.delete()
