# Arquivo contendo as funções de serviço.
# Autenticação, criação de token e etc.

import schemas as _schemas, models as _models, database as _database

from typing import Annotated
from jose import JWTError, jwt

from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext

from sqlalchemy.orm import Session

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "cfc815eabd4982df1bc5ef0407d0ae0c211c2189f0f8d5aaadd257dd8e45d824"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db: Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()

async def get_user_by_username(db: Session, username: str):
    return db.query(_models.User).filter(_models.User.username == username).first()

async def create_user(user: _schemas.UserCreate, db: Session):
    user_obj = _models.User(
        username=user.username,
        hashed_password=get_password_hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(db: Session, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = await get_user_by_username(db, payload["sub"])
    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )
    return _schemas.User.from_orm(user)

async def get_addresses(db: Session, user: _schemas.User):
    addresses = db.query(_models.Address).filter_by(owner_id = user.id)
    return list(map(_schemas.Address.from_orm, addresses))