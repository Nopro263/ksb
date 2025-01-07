from typing import Optional
from typing_extensions import Self
import inspect

from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr

class _Nickname(BaseModel):
    nickname: str

class _PrivateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    def set_from(self, data: Self):
        model_fields = { name:value for name, value in inspect.getmembers(_PrivateUser, lambda a:not(inspect.isroutine(a))) if not name.startswith("_")}["model_fields"]

        for name, field in model_fields.items():
            print(name, getattr(data, name))
            setattr(self, name, getattr(data, name))

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