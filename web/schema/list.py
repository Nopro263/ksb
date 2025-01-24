from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class _List(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(default=None, foreign_key="users.id")
    id_in_user: int

class List(_List, SQLModel, table=True):
    __tablename__ = "list"