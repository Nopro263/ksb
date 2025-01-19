from fastapi import APIRouter, Body, HTTPException
from typing import Annotated, List
from sqlmodel import select, or_, and_

from ..schema.models import LoginResponse
from ..schema.article import Article
from ..schema.list import List as _List
from ..schema.user import CreatingUser, PrivateUser, _PrivateUser, User, Config, get_config_for_user
from ..security import FormData, Auth, Clearance, encode, hash

from ..database import DB

router = APIRouter(prefix="/user")

usernames = ["Apfel", "Birne", "Vogelbeere", "Marille", "Olive", "Zwetschge", "Pfirsich", "Kirsche", "Brombeere", "Erdbeer", "Weintraube", "Erdnuss", "Ananas", "Avokado", "Banane", "Orange", "Kiwi", "Mandarine", "Dattel", "Kokosnuss", "Ingwer", "Feige", "Melone", "Papaya", "Pistazie"]

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
async def getData(db: DB, auth: Auth[Clearance.REGISTERED]) -> PrivateUser:
    return auth.get_user(db)

@router.get("/config")
async def getConfig(auth: Auth[Clearance.REGISTERED]) -> Config:
    return get_config_for_user(auth)

@router.post("/me")
async def setData(db: DB, auth: Auth[Clearance.REGISTERED], user: Annotated[_PrivateUser, Body()]):
    old_user = auth.get_user(db)
    old_user.set_from(_PrivateUser, user)
    db.commit()

@router.get("/users")
async def getUsers(db: DB, auth: Auth[Clearance.EMPLOYEE]) -> List[PrivateUser]:
    return db.exec(select(User)).all()

@router.get("/{id:int}")
async def getUser(db: DB, id: int, auth: Auth[Clearance.EMPLOYEE]) -> PrivateUser:
    return db.exec(select(User).where(User.id == id)).one()

@router.get("/{id:int}/articles")
async def getArticles(db: DB, auth: Auth[Clearance.EMPLOYEE], id:int) -> List[Article]:
    r = []
    for article, _ in db.exec(select(Article, _List).where(and_(Article.list_id == _List.id, _List.owner_id == id)).order_by(Article.id)).all():
        r.append(article)

    return r