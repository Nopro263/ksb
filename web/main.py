from fastapi import FastAPI, Depends, HTTPException
import fastapi.security
from database import DB
from schema.user import User, PrivateUser, CreatingUser
from schema.article import Article
from schema.invoice import Invoice
from schema.list import List
from sqlmodel import select, insert
from typing import Annotated, Sequence
from utils import Error, Auth, Clearance, encode
import hashlib
import time


from datetime import datetime

app = FastAPI()

def hash(d: str) -> str:
    d = d.encode("utf-8")
    return hashlib.sha512(d).hexdigest()


@app.get("/users")
def get_all_users(db: DB) -> Sequence[PrivateUser]:
    expr = select(User)
    result = db.exec(expr)

    return result.fetchall()

@app.get("/articles")
def get_all_users(db: DB) -> Sequence[Article]:
    expr = select(Article)
    result = db.exec(expr)

    return result.fetchall()

@app.get("/invoices")
def get_all_users(db: DB) -> Sequence[Invoice]:
    expr = select(Invoice)
    result = db.exec(expr)

    return result.fetchall()

@app.get("/lists")
def get_all_users(db: DB) -> Sequence[List]:
    expr = select(List)
    result = db.exec(expr)

    return result.fetchall()

@app.post("/token")
def token(db: DB, form_data: Annotated[fastapi.security.OAuth2PasswordRequestForm, Depends()]) -> dict:

    user = db.exec(select(User).where((User.email == form_data.username or User.nickname == form_data.username) and User.password == hash(form_data.password))).first()

    if not user:
        raise HTTPException(status_code=403, detail="Username/Password is wrong")

    return {"access_token": encode(Clearance(user.clearance), user.id), "token_type": "bearer"}

@app.post("/register", responses={
    409: Error(description="Nickname exists already")
})
def register(db: DB, user: CreatingUser) -> PrivateUser:
    result = db.exec(select(User).where(User.nickname == user.nickname))

    if result.fetchall():
        raise HTTPException(status_code=409, detail="Nickname exists already")

    _user = User.model_validate(user)
    _user.password = hash(user.password)
    db.add(_user)
    db.commit()
    db.refresh(_user)

    return _user

@app.put("/invoice")
def put_invoice(db: DB) -> Invoice:
    _invoice = Invoice(creation_time=datetime.now())
    db.add(_invoice)
    db.commit()
    db.refresh(_invoice)

    return _invoice

@app.post("/invoice/{invoice_id:int}")
def sell_invoice(db: DB, article_id: int, invoice_id: int, auth: Auth[Clearance.EMPLOYEE]) -> None:
    result = db.exec(select(Article).where(Article.id == article_id)).first()
    print(auth)
    result.invoice_id = invoice_id

    db.add(result)
    db.commit()

@app.get("/invoice/{invoice_id:int}")
def get_invoice(db: DB, invoice_id: int) -> Sequence[Article]:
    expr = select(Article).where(Article.invoice_id == invoice_id)
    result = db.exec(expr)

    return result.fetchall()