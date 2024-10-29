from typing import Annotated, Tuple
from fastapi import Depends, HTTPException

from enum import IntEnum
import jwt
from sqlmodel import Session, select
from .schema.user import User

from . import config
import fastapi.security
import datetime
import hashlib

from pydantic import BaseModel

flow = fastapi.security.OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="bearer")

class Clearance(IntEnum):
    ADMIN = 99,
    EMPLOYEE = 50,
    REGISTERED = 10,
    OTHER = 0

class ClearedUser(BaseModel):
    clearance: Clearance
    userId: int

    def get_user(self, db: Session) -> User:
        return db.exec(select(User).where(User.id == self.userId)).one()

def encode(cl: Clearance, userid: int) -> str:
    return jwt.encode({
        "expires": (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat(),
        "clearance": int(cl), 
        "userid": userid
    }, config.secret)

def decode(s: str) -> Tuple[Clearance, int]:
    try:
        data = jwt.decode(s, config.secret, algorithms=["HS256"])
    except Exception:
        return None
    
    expires = datetime.datetime.fromisoformat(data["expires"])
    
    if expires < datetime.datetime.now():
        return None
    
    return (Clearance(data["clearance"]), data["userid"])

def hash(d: str) -> str:
    d = d.encode("utf-8")
    return hashlib.sha512(d).hexdigest()


class Auth(ClearedUser):
    def __class_getitem__(cls, clearance):
        def f(token: Annotated[str, fastapi.Depends(flow)]):
            try:
                cl, userid = decode(token)
            except Exception:
                raise HTTPException(status_code=401, detail="Token can not be decoded")
            
            if cl < clearance:
                raise HTTPException(status_code=403, detail="No access")
            
            return ClearedUser(clearance=cl, userId=userid)

        return Annotated[ClearedUser, Depends(f)]

FormData = Annotated[fastapi.security.OAuth2PasswordRequestForm, Depends()]