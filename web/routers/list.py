import datetime

from fastapi import APIRouter, Body
from typing import Annotated

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
    a = Article(**article.model_dump(), imported=False, list_id=listId)
    db.add(a)
    db.commit()
    db.refresh(a)

    return a

@router.delete("/{listId}/{articleId}")
async def deleteArticle():
    pass