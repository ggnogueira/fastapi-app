from datetime import datetime, timedelta
from typing import Annotated

from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status

import services as _services, schemas as _schemas

from sqlalchemy.orm import Session
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/token", response_model=_schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(_services.get_db)]
):
    user = await _services.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await _services.create_access_token(
        data={"sub": user.username, "role": "User", "id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/users")
async def create_user(
    user: _schemas.UserCreate,
    db: Annotated[Session, Depends(_services.get_db)]
):
    db_user = await _services.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists in the database"
        )
    user = await _services.create_user(user, db)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return await _services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

@app.get("/api/v1/users/me/", response_model=_schemas.User)
async def read_users_me(
    current_user: Annotated[_schemas.User, Depends(_services.get_current_user)]
):
    return current_user

@app.get("/api/v1/users/{user_id}", status_code=200)
async def get_user(
    user: Annotated[_schemas.User, Depends(_services.get_current_user)],
    db: Annotated[Session, Depends(_services.get_db)]
):
    return await _services.get_user(db, user.id)

@app.get("/api/v1/users/me/addresses/")
async def read_own_address(
    current_user: Annotated[_schemas.User, Depends(_services.get_current_user)],
    db: Annotated[Session, Depends(_services.get_db)]
):
    addresses = await _services.get_addresses(db, current_user)
    return addresses