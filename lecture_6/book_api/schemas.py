from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]  # String type that must be non-empty after whitespace removal


class BookCreate(BaseModel):
    title: NonEmptyStr
    author: NonEmptyStr
    year: Optional[int] = Field(None, ge=0)


class BookUpdate(BaseModel):
    title: Optional[NonEmptyStr] = None
    author: Optional[NonEmptyStr] = None
    year: Optional[int] = Field(None, ge=0)


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Enable conversion from SQLAlchemy ORM models

    id: int
    title: str
    author: str
    year: Optional[int]
