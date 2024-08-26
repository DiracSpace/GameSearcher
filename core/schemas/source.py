from pydantic import BaseModel, HttpUrl

from core.schemas.consle_type import ConsoleTypeEnum


class SourceSchema(BaseModel):
    key: ConsoleTypeEnum = ConsoleTypeEnum.unknown
    value: HttpUrl
