from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class PublicUser(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    nickname: str

class PrivateUser(PublicUser):
    first_name: str
    last_name: str
    email: str

class User(PrivateUser, SQLModel, table=True):
    __tablename__ = "users"

    password: str
    