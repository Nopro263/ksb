import config
from sqlmodel import create_engine, Session

from typing import Annotated, Any
from fastapi import Depends

engine = create_engine(f"{config.db_type}://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_database}")

class _DB:
    def __init__(self) -> None:
        self.ctx = Session(engine)

    def __enter__(self) -> None:
        self.ctx.__enter__()

    def __exit__(self, type, value, traceback) -> None:
        self.ctx.__exit__(type, value, traceback)
    
    def __call__(self) -> Any:
        return self.ctx

DB = Annotated[Session, Depends(_DB())]