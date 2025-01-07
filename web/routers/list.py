from fastapi import APIRouter, Body
from typing import Annotated

from ..database import DB
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

@router.post("/{listId}")
async def createArticle():
    pass

@router.delete("/{listId}/{articleId}")
async def deleteArticle():
    pass