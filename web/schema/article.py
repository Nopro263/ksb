from typing import Optional

from sqlmodel import Field, SQLModel, ForeignKey
from .models import _Base

class CreateArticle(_Base):
    name: str
    barcode: int
    size: str
    price: int


class Article(CreateArticle, SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    imported: bool
    deleted: bool
    list_id: int = Field(default=None, foreign_key="list.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")