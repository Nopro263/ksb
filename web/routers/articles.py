import io

from barcode.writer import SVGWriter
from fastapi import APIRouter
from sqlmodel import select
import barcode
from starlette.responses import Response

from ..database import DB
from ..schema.article import Article

router = APIRouter(prefix="/article")

@router.get("/{id:int}/barcode/")
def gen_barcode(db: DB, id:int):
    article = db.exec(select(Article).where(Article.id == id)).one()
    ean = barcode.ean.EAN13(str(article.barcode), writer=SVGWriter())
    buffer = io.BytesIO()
    ean.write(buffer)
    return Response(content=buffer.getvalue(), media_type="image/svg+xml")