from typing import Optional
from datetime import datetime

from sqlmodel import Field, SQLModel


class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"

    id: Optional[int] = Field(default=None, primary_key=True)
    creation_time: datetime