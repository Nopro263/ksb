import config
from sqlmodel import create_engine, Session

from typing import Annotated, Any
from fastapi import Depends

engine = create_engine(f"{config.db_type}://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_database}")

def _get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

DB = Annotated[Session, Depends(_get_db)]