from fastapi import FastAPI
from .routers.users import router as users_router
from .routers.list import router as list_router
from .routers.articles import router as articles_router

app = FastAPI()

app.include_router(users_router)
app.include_router(list_router)
app.include_router(articles_router)