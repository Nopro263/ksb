from fastapi import FastAPI, Depends
from database import DB
from schema.user import User, PrivateUser
from schema.article import Article
from schema.invoice import Invoice
from schema.list import List
from sqlmodel import select
from typing import Sequence

app = FastAPI()

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