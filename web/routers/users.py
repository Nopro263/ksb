from fastapi import APIRouter, Body, HTTPException
from typing import Annotated, List
from sqlmodel import select, or_

from ..schema.user import CreatingUser, PrivateUser, _PrivateUser, User
from ..schema.models import LoginResponse
from ..security import FormData, Auth, Clearance, encode, hash

from ..database import DB

router = APIRouter(prefix="/user")

usernames = ["Ananas", "Kiwi", "Apfel", "Mango", "Birne", "Melone", "Banane", "Nopro"]

def get_usernames(db):
    us = usernames.copy()
    for name in db.exec(select(User.nickname)).all():
        try:
            us.remove(name)
        except ValueError:
            pass
    return us

@router.get("/usernames")
async def getAvailableUsernames(db: DB) -> List[str]:
    return get_usernames(db)

@router.put("/register")
async def register(db: DB, user: Annotated[CreatingUser, Body()]) -> PrivateUser:
    if user.nickname not in get_usernames(db):
        raise HTTPException(status_code=404, detail="Nickname not in allowed list")

    result = db.exec(select(User).where(or_(User.nickname == user.nickname, User.email == user.email)))

    if result.fetchall():
        raise HTTPException(status_code=409, detail="Nickname already exists")

    _user = User.model_validate(user)
    _user.password = hash(user.password)
    db.add(_user)
    db.commit()
    db.refresh(_user)
    db.commit()

    return _user

@router.post("/login")
async def login(db: DB, user: FormData) -> LoginResponse:
    user = db.exec(select(User).where(
        or_(User.email == user.username, 
            User.nickname == user.username)
        ).where(
            User.password == hash(user.password)
        )).first()

    if not user:
        raise HTTPException(status_code=403, detail="Username/Password is wrong")

    return LoginResponse(access_token=encode(Clearance(user.clearance), user.id))

@router.get("/me")
async def getData(db: DB, auth: Auth[Clearance.OTHER]) -> PrivateUser:
    return auth.get_user(db)

@router.post("/me")
async def setData(db: DB, auth: Auth[Clearance.OTHER], user: Annotated[_PrivateUser, Body()]):
    old_user = auth.get_user(db)
    old_user.set_from(user)
    db.commit()
