import datetime
import hashlib
import os
from typing import Union, List

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import select
from starlette.datastructures import URL
from starlette.requests import Request

from ..database import DB
from ..schema.article import Article
from ..schema.invoice import Invoice
from ..schema.models import SellResponse
from ..security import Clearance, Auth
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/invoice")

templates = Jinja2Templates(directory="templates")

secrets = {}

@router.post("/new")
def new_invoice(db: DB, auth: Auth[Clearance.EMPLOYEE]) -> Invoice:
    inv = Invoice(creation_time=datetime.datetime.now())

    db.add(inv)
    db.commit()
    db.refresh(inv)

    return inv

@router.post("/{id:int}/sell/{article:int}")
def sell_article(db: DB, auth: Auth[Clearance.EMPLOYEE], id: int, article: int) -> SellResponse:
    if len(str(article)) == 13:
        article = str(article)[:-1]
    _bc = str(article).rjust(12, "0")
    a: Article = db.exec(select(Article).where(Article.barcode == _bc)).one()
    invoice_id = a.invoice_id

    sr = SellResponse.model_validate(a, from_attributes=True, update={"has_already_been_sold": isinstance(invoice_id, int)})

    if isinstance(invoice_id, int):
        return sr

    a.invoice_id = id
    db.commit()
    db.refresh(a)

    

    return sr

@router.get("/{id:int}")
def get_invoice(db: DB, auth: Auth[Clearance.EMPLOYEE], id: int) -> List[Article]:
    return db.exec(select(Article).where(Article.invoice_id == id)).all()

@router.get("/{id:int}/meta")
def get_invoice(db: DB, auth: Auth[Clearance.EMPLOYEE], id: int) -> Invoice:
    return db.exec(select(Invoice).where(Invoice.id == id)).one()

@router.get("/{id:int}/print")
def get_print_invoice_link(db: DB, auth: Auth[Clearance.EMPLOYEE], id: int, request: Request) -> str:
    s = hashlib.sha256(f"{id}{os.environ['SECRET']}".encode("utf-8")).hexdigest()
    secrets[id] = s
    return str(request.url_for("print_invoice", id=id, secret=s))

@router.get("/{id:int}/print/{secret:str}")
def print_invoice(db: DB, id: int, secret: str, request: Request) -> HTMLResponse:
    if id not in secrets or secrets[id] != secret:
        raise HTTPException(status_code=403, detail="invalid print secret")
    del secrets[id]

    invoice = db.exec(select(Invoice).where(Invoice.id == id)).one()
    articles = db.exec(select(Article).where(Article.invoice_id == id)).all()

    s = sum([a.price for a in articles])

    return templates.TemplateResponse("invoice.html", {"invoice": invoice, "articles": articles, "request": request, "data": {"sum":s}})