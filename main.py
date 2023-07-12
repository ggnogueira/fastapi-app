from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import services as _services, schemas as _schemas

ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

@app.post("/api/v1/token", response_model=_schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = _services.authenticate_user(_services.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/users/me/", response_model=_schemas.User)
async def read_users_me(
    current_user: Annotated[_schemas.User, Depends(_services.get_current_active_user)]
):
    return current_user

@app.get("/api/v1/users/me/items/")
async def read_own_items(
    current_user: Annotated[_schemas.User, Depends(_services.get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]