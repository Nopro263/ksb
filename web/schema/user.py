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

from ..security import Clearance, ClearedUser

class Config(BaseModel):
    max_lists: int
    max_items_per_list: int
    is_employee: bool

def get_config_for_user(user: ClearedUser) -> Config:
    return Config(
        max_lists=3,
        max_items_per_list=60,
        is_employee=user.clearance >= Clearance.EMPLOYEE
    )