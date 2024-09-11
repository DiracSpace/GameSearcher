from typing import List
from beanie import Link
from pydantic import BaseModel, Field

from backend.features.parsers.models import ParserDocument


class Review(BaseModel):
    comment: str
    rating: int = Field(..., gt=0, le=5)


class Rating(BaseModel):
    parserId: Link[ParserDocument]
    trust: int = Field(..., gt=0, le=5)
    performance: int = Field(..., gt=0, le=5)
    reviews: List[Review]
