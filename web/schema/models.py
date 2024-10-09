from pydantic import BaseModel

from .article import Article

class ArticleId(BaseModel):
    articleId: int

class ImportResponse(Article):
    has_already_been_imported: bool