from typing import Optional
from typing_extensions import Self
import inspect

from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr

from .models import _Base


class _Nickname(BaseModel):
    nickname: str

class _PrivateUser(_Base):
    first_name: str
    last_name: str
    email: EmailStr

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

    clearance: int = Field(default=10)