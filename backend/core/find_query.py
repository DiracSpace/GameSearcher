from typing import ClassVar
from attr import dataclass
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class FindQuery(BaseModel):
    page_index: Annotated[int, Field(validate_default=True)] = 0
    page_size: Annotated[int, Field(validate_default=True)] = 10
    filter: Annotated[str, Field(validate_default=True)] = ""
    order_by: str = ""

    # TODO: implement a pattern to turn a string filter into a mapping of property and value
    supported_operators: ClassVar[list[str]] = [
        "eq",
        "ne",
        "in",
        "nin",
        "gt",
        "lt",
        "gte",
        "lte",
        "&&",
        "||",
        "<",
        ">",
    ]

    @property
    def skip(self):
        return self.page_index * self.page_size

    @property
    def limit(self):
        return self.page_size

    @field_validator("page_index", "page_size")
    @classmethod
    def validate_pagination(cls, value: int) -> int:
        if value < 0:
            raise ValueError("value must not be less than {default_value}", 0)

        return value

    @field_validator("filter")
    @classmethod
    def validate_filter(cls, value: str) -> str:
        operators = [word for word in value.strip() if word in cls.supported_operators]
        for operator in operators:
            if operator not in cls.supported_operators:
                raise ValueError(f"Unsupported operator: {operators}")

        return value
