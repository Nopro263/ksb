from fastapi import FastAPI

from .routers.users import router as users_router
from .routers.list import router as list_router
from .routers.articles import router as articles_router
from .routers.invoice import router as invoice_router

from .database import DB
from .security import Auth, Clearance
from .schema.models import StatsResponse
from .schema.article import Article

from sqlmodel import func, select

app = FastAPI()

app.include_router(users_router)
app.include_router(list_router)
app.include_router(articles_router)
app.include_router(invoice_router)

@app.get("/stats")
def stats(db: DB, auth: Auth[Clearance.EMPLOYEE]) -> StatsResponse:
    amount_articles = db.exec(select(func.count()).where(Article.deleted == False)).one()
    imported = db.exec(select(func.count()).where(Article.imported == True)).one()
    sold = db.exec(select(func.count()).where(Article.invoice_id != None)).one()
    sold_value = db.exec(select(func.sum(Article.price)).where(Article.invoice_id != None)).one()
    total_value = db.exec(select(func.sum(Article.price)).where(Article.deleted == False)).one()

    return StatsResponse(
        imported=imported,
        amount_articles=amount_articles,
        sold=sold,
        sold_value=sold_value,
        total_value=total_value
    )