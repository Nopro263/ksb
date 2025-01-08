import datetime

from fastapi import APIRouter, Body, HTTPException
from typing import Annotated

from sqlmodel import select

from ..database import DB
from ..schema.article import CreateArticle, Article
from ..schema.invoice import Invoice
from ..schema.list import List
from ..security import Auth, Clearance

router = APIRouter(prefix="/list")

@router.put("/")
async def createList(db: DB, auth: Auth[Clearance.OTHER]) -> List:
    l = List(owner_id=auth.userId)
    db.add(l)
    db.commit()
    db.refresh(l)

    return l

@router.post("/{listId:int}")
async def createArticle(db: DB, listId: int, auth: Auth[Clearance.OTHER], article: CreateArticle) -> Article:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")
    a = Article(**article.model_dump(), imported=False, list_id=listId)
    db.add(a)
    db.commit()
    db.refresh(a)

    return a

@router.delete("/{listId}/{articleId}")
async def deleteArticle(db: DB, listId: int, articleId: int, auth: Auth[Clearance.OTHER]) -> str:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")

    article = db.exec(select(Article).where(Article.id == articleId))
    article.deleted = True
    db.commit()

    return "ok"