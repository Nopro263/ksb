from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class _Nickname(BaseModel):
    nickname: str

class _PrivateUser(BaseModel):
    first_name: str
    last_name: str
    email: str

class _Password(BaseModel):
    password: str

class PublicUser(_Nickname):
    id: Optional[int] = Field(default=None, primary_key=True)

class PrivateUser(PublicUser, _PrivateUser):
    pass

class CreatingUser(_PrivateUser, _Nickname, _Password):
    pass


class User(PrivateUser, _Password, SQLModel, table=True):
    __tablename__ = "users"