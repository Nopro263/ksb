import io

from barcode.writer import SVGWriter
from fastapi import APIRouter, HTTPException
from sqlmodel import select, col, or_
import barcode
from starlette.responses import Response
from sqlalchemy.exc import NoResultFound

from ..security import Auth, Clearance

from ..database import DB
from ..schema.article import Article
from ..schema.models import ImportResponse, SearchRequest

router = APIRouter(prefix="/article")

@router.get("/{id:int}/barcode/")
def gen_barcode(db: DB, id:int):
    article = db.exec(select(Article).where(Article.id == id)).one()
    ean = barcode.ean.EAN13(str(article.barcode), writer=SVGWriter())
    buffer = io.BytesIO()
    ean.write(buffer)
    return Response(content=buffer.getvalue(), media_type="image/svg+xml")

@router.post("/{bc:int}/import/")
def import_article(db: DB, bc:int) -> ImportResponse:
    if len(str(bc)) == 13:
        bc = str(bc)[:-1]
    _bc = str(bc).rjust(12, "0")
    try:
        article: Article = db.exec(select(Article).where(Article.barcode == _bc)).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Artikel nicht gefunden")
    imported = article.imported

    article.imported = True
    db.commit()

    ir = ImportResponse.model_validate(article, from_attributes=True, update={"has_already_been_imported": imported})

    return ir

@router.post("/search")
def search_article(db: DB, auth: Auth[Clearance.EMPLOYEE], query: SearchRequest) -> list[Article]:
    response = []
    try:
        response = db.exec(select(Article).where(or_(col(Article.name).contains(query.query), col(Article.size).contains(query.query), Article.barcode == query.query, Article.id_in_list == int(query.query), Article.invoice_id == int(query.query))))
    except Exception:
        response = db.exec(select(Article).where(or_(col(Article.name).contains(query.query), col(Article.size).contains(query.query), Article.barcode == query.query))).all()
    
    return response