import datetime
import os
from typing import Optional

from sqlmodel import Field, SQLModel, ForeignKey
from .models import _Base

class CreateArticle(_Base):
    name: str
    size: str
    price: float


class Article(CreateArticle, SQLModel, table=True):
    __tablename__ = "articles"

    id: Optional[int] = Field(default=None, primary_key=True)
    imported: bool
    deleted: bool
    barcode: Optional[str] = None
    list_id: int = Field(default=None, foreign_key="list.id")
    invoice_id: Optional[int] = Field(default=None, foreign_key="invoice.id")

    def gen_barcode(self):
        year = datetime.datetime.now().year
        count_in_year = int(os.environ["COUNT_IN_YEAR"])
        self.barcode = f"{int(year) % 100}{count_in_year % 10}{str(self.id).rjust(6, '0')}{str(self.list_id).rjust(3, '0')}".ljust(12, "0")