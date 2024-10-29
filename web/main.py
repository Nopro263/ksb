from fastapi import FastAPI
from .routers.users import router as users_router
from .routers.list import router as list_router


app = FastAPI()

app.include_router(users_router)
app.include_router(list_router)