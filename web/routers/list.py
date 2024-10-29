from fastapi import APIRouter, Body
from typing import Annotated

router = APIRouter(prefix="/list")

@router.put("/")
async def createList():
    pass

@router.post("/{listId}")
async def createArticle():
    pass

@router.delete("/{listId}/{articleId}")
async def deleteArticle():
    pass