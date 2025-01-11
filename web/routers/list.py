import datetime

import barcode
from fastapi import APIRouter, Body, HTTPException
from typing import Annotated, List as _List

from sqlmodel import select

from ..database import DB
from ..schema.article import CreateArticle, Article
from ..schema.invoice import Invoice
from ..schema.list import List
from ..schema.models import ListResponse
from ..security import Auth, Clearance

router = APIRouter(prefix="/list")

@router.put("/")
async def createList(db: DB, auth: Auth[Clearance.REGISTERED]) -> List:
    l = List(owner_id=auth.userId)
    db.add(l)
    db.commit()
    db.refresh(l)

    return l

@router.get("/")
async def getLists(db: DB, auth: Auth[Clearance.REGISTERED]) -> _List[List]:
    return db.exec(select(List).where(List.owner_id == auth.userId)).all()

@router.post("/{listId:int}")
async def createArticle(db: DB, listId: int, auth: Auth[Clearance.REGISTERED], article: CreateArticle) -> Article:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")
    a = Article(**article.model_dump(), imported=False, list_id=listId, deleted=False)
    db.add(a)
    db.commit()
    db.refresh(a)

    a.gen_barcode()
    db.commit()
    db.refresh(a)

    return a

@router.get("/{listId:int}")
async def getList(db: DB, listId: int, auth: Auth[Clearance.REGISTERED]) -> ListResponse:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")

    articles = db.exec(select(Article).where(Article.list_id == listId))

    return ListResponse(**list.model_dump(), articles=articles)

@router.delete("/{listId}/{articleId}")
async def deleteArticle(db: DB, listId: int, articleId: int, auth: Auth[Clearance.REGISTERED]) -> str:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")

    article: Article = db.exec(select(Article).where(Article.id == articleId)).one()
    article.deleted = True
    db.commit()
    db.refresh(article)

    return "ok"