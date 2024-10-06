from typing import Optional

from sqlmodel import Field, SQLModel, ForeignKey


class Article(SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    barcode: int
    imported: bool
    list_id: int = Field(default=None, foreign_key="list.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoices.id")