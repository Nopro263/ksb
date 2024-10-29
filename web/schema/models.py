from pydantic import BaseModel

from .article import Article

class ArticleId(BaseModel):
    articleId: int

class ImportResponse(Article):
    has_already_been_imported: bool

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"