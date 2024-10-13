from fastapi import FastAPI, Depends, HTTPException, Body
import fastapi.security
from database import DB
from schema.user import User, PrivateUser, CreatingUser
from schema.article import Article
from schema.invoice import Invoice
from schema.list import List

from schema.models import ArticleId, ImportResponse

from sqlmodel import select, insert, or_
from typing import Annotated, Sequence
from utils import Error, Auth, Clearance, encode
import hashlib
import time


from datetime import datetime

app = FastAPI()

def hash(d: str) -> str:
    d = d.encode("utf-8")
    return hashlib.sha512(d).hexdigest()



@app.post("/token")
def token(db: DB, form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, Depends()]) -> dict:

    user = db.exec(select(User).where(
        or_(User.email == form_data.username, 
            User.nickname == form_data.username)
        ).where(
            User.password == hash(form_data.password)
        )).first()

    if not user:
        raise HTTPException(status_code=403, detail="Username/Password is wrong")

    return {"access_token": encode(Clearance(user.clearance), user.id), "token_type": "bearer"}

@app.post("/register", responses={
    409: Error(description="Nickname already exists")
})
def register(db: DB, user: CreatingUser) -> PrivateUser:
    result = db.exec(select(User).where(User.nickname == user.nickname))

    if result.fetchall():
        raise HTTPException(status_code=409, detail="Nickname already exists")

    _user = User.model_validate(user)
    _user.password = hash(user.password)
    db.add(_user)
    db.commit()
    db.refresh(_user)

    return _user

@app.put("/invoice")
def put_invoice(db: DB, auth: Auth[Clearance.EMPLOYEE]) -> Invoice:
    _invoice = Invoice(creation_time=datetime.now())
    db.add(_invoice)
    db.commit()
    db.refresh(_invoice)

    return _invoice

@app.post("/invoice/{invoice_id:int}")
def sell_invoice(db: DB, article_id: int, invoice_id: int, auth: Auth[Clearance.EMPLOYEE]) -> None:
    result = db.exec(select(Article).where(Article.id == article_id)).first()
    result.invoice_id = invoice_id

    db.add(result)
    db.commit()

@app.get("/invoice/{invoice_id:int}")
def get_invoice(db: DB, invoice_id: int, auth: Auth[Clearance.EMPLOYEE]) -> Sequence[Article]:
    expr = select(Article).where(Article.invoice_id == invoice_id)
    result = db.exec(expr)

    return result.fetchall()

@app.post("/import")
def import_article(db: DB, article_id: ArticleId, auth: Auth[Clearance.EMPLOYEE]) -> ImportResponse:
    expr = select(Article).where(Article.id == article_id.articleId)
    result = db.exec(expr).one()

    if result.imported:
        return ImportResponse(**result.model_dump(), has_already_been_imported=True)

    result.imported = True

    db.add(result)
    db.commit()
    db.refresh(result)

    return ImportResponse(**result.model_dump(), has_already_been_imported=False)