from uuid import UUID
from pydantic import BaseModel
from pydantic import Field
from typing import Optional

class Schema(BaseModel): ...

class User(Schema):
    id: UUID = Field(...)
    username: str = Field(...)

class Account(Schema):
    id: str = Field(...)
    type: str = Field(...)
    provider: str = Field(...)