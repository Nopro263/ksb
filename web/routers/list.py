import datetime
import hashlib
import os

import barcode
from fastapi import APIRouter, Body, HTTPException, Request
from typing import Annotated, List as _List

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select, and_

from ..schema.user import User, get_config_for_user

from ..database import DB
from ..schema.article import CreateArticle, Article
from ..schema.invoice import Invoice
from ..schema.list import List
from ..schema.models import ListResponse
from ..security import Auth, Clearance

secrets = {}

templates = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/list")

@router.put("/")
async def createList(db: DB, auth: Auth[Clearance.REGISTERED]) -> List:
    config = get_config_for_user(auth)
    lists = len(db.exec(select(List.id).where(List.owner_id == auth.userId)).all())

    if(lists+1 > config.max_lists):
        raise HTTPException(status_code=402, detail=f"no more than {config.max_lists} lists are allowed")

    l = List(owner_id=auth.userId, id_in_user=lists+1)
    db.add(l)
    db.commit()
    db.refresh(l)

    return l

@router.get("/")
async def getLists(db: DB, auth: Auth[Clearance.REGISTERED]) -> _List[List]:
    return db.exec(select(List).where(List.owner_id == auth.userId)).all()

@router.get("/of/{userId:int}")
async def getListsOfUser(db: DB, auth: Auth[Clearance.EMPLOYEE], userId: int) -> _List[List]:
    return db.exec(select(List).where(List.owner_id == userId)).all()

@router.post("/{listId:int}")
async def createArticle(db: DB, listId: int, auth: Auth[Clearance.REGISTERED], article: CreateArticle) -> Article:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")
    
    config = get_config_for_user(auth)
    articles = len(db.exec(select(Article.id).where(and_(Article.list_id == listId, Article.deleted == False)).order_by(Article.id)).all())
    all_articles = len(db.exec(select(Article.id).where(Article.list_id == listId).order_by(Article.id)).all())

    if(articles+1 > config.max_items_per_list):
        raise HTTPException(status_code=402, detail=f"no more than {config.max_items_per_list} items are allowed per list")

    a = Article(**article.model_dump(), imported=False, list_id=listId, deleted=False, id_in_list=all_articles+1)
    db.add(a)
    db.commit()
    db.refresh(a)

    a.gen_barcode()
    db.commit()
    db.refresh(a)

    return a

@router.get("/{listId:int}/bypass")
async def getList(db: DB, listId: int, auth: Auth[Clearance.EMPLOYEE]) -> ListResponse:
    list = db.exec(select(List).where(List.id == listId)).one()

    articles = db.exec(select(Article).where(Article.list_id == listId).order_by(Article.id))

    return ListResponse(**list.model_dump(), articles=articles)

@router.get("/{listId:int}")
async def getList(db: DB, listId: int, auth: Auth[Clearance.REGISTERED]) -> ListResponse:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")

    articles = db.exec(select(Article).where(Article.list_id == listId).order_by(Article.id))

    return ListResponse(**list.model_dump(), articles=articles)

@router.delete("/{listId:int}/{articleId}")
async def deleteArticle(db: DB, listId: int, articleId: int, auth: Auth[Clearance.REGISTERED]) -> str:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")

    article: Article = db.exec(select(Article).where(Article.id == articleId)).one()
    article.deleted = True
    db.commit()
    db.refresh(article)

    return "ok"


@router.get("/{listId:int}/print")
def get_print_list_link(db: DB, auth: Auth[Clearance.REGISTERED], listId: int, request: Request) -> str:
    list = db.exec(select(List).where(List.id == listId)).one()
    if list.owner_id != auth.userId:
        raise HTTPException(status_code=403, detail="not your list")
    
    s = hashlib.sha256(f"{listId}{os.environ['SECRET']}".encode("utf-8")).hexdigest()
    secrets[listId] = s
    return str(request.url_for("print_list", listId=listId, secret=s))

@router.get("/{listId:int}/print/{secret:str}")
def print_list(db: DB, listId: int, secret: str, request: Request) -> HTMLResponse:
    if listId not in secrets or secrets[listId] != secret:
        raise HTTPException(status_code=403, detail="invalid print secret")
    del secrets[listId]

    list = db.exec(select(List).where(List.id == listId)).one()
    user = db.exec(select(User).where(User.id == list.owner_id)).one()
    articles = db.exec(select(Article).where(Article.list_id == listId).order_by(Article.id)).all()


    s = sum([a.price for a in articles if not a.deleted])
    ar = sum([1 for a in articles if not a.deleted])

    return templates.TemplateResponse("list.html", {"list": list, "articles": articles, "request": request, "user": user, "data": {"sum":s, "amount":ar}})