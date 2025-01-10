import inspect
from typing import Any, List as L

from pydantic import BaseModel

class _Base(BaseModel):
    def set_from(self, cls, data: Any):
        model_fields = { name:value for name, value in inspect.getmembers(cls, lambda a:not(inspect.isroutine(a))) if not name.startswith("_")}["model_fields"]

        for name, field in model_fields.items():
            setattr(self, name, getattr(data, name))

from .article import Article

class ArticleId(BaseModel):
    articleId: int

class ImportResponse(Article):
    has_already_been_imported: bool

class SellResponse(Article):
    has_already_been_sold: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

from .list import _List

class ListResponse(_List):
    articles: L[Article]