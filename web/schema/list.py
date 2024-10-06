from typing import Optional

from sqlmodel import Field, SQLModel


class List(SQLModel, table=True):
    __tablename__ = "list"

    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(default=None, foreign_key="users.id")