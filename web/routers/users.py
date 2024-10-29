from fastapi import APIRouter, Body
from typing import Annotated, List

from ..schema.user import CreatingUser, PrivateUser, _PrivateUser
from ..schema.models import LoginResponse
from ..security import FormData, Auth, Clearance

router = APIRouter(prefix="/user")

@router.get("/usernames")
async def getAvailableUsernames() -> List[str]:
    return ["Ananas", "Kiwi", "Apfel", "Mango", "Birne", "Melone", "Banane"]

@router.put("/register")
async def register(user: Annotated[CreatingUser, Body()]) -> PrivateUser:
    return PrivateUser(**user.model_dump(), id=0)

@router.post("/login")
async def login(user: FormData) -> LoginResponse:
    return LoginResponse(access_token="abc")

@router.get("/me")
async def getData(auth: Auth[Clearance.OTHER]) -> PrivateUser:
    pass

@router.post("/me")
async def setData(auth: Auth[Clearance.OTHER], user: Annotated[_PrivateUser, Body()]):
    pass