from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from uuid import UUID

from backend.core.find_query import FindQuery


# Define a type variable for the model
T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def get_all(self, query: FindQuery) -> List[T]:
        pass

    @abstractmethod
    async def get_by_id(self, id: UUID) -> T:
        pass

    @abstractmethod
    async def get_by_id_or_default(self, id: UUID) -> T | None:
        pass

    @abstractmethod
    async def create(self, model: T) -> UUID:
        pass

    @abstractmethod
    async def update(self, model: T):
        pass

    @abstractmethod
    async def delete(self, id: UUID):
        pass
