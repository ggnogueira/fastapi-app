# Arquivo contendo os schemas.
from datetime import datetime, timedelta
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class AddressBase(BaseModel):
    city: str
    country: str
    street: str
    postal: str
    type: str

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    username: str
    first_name: str | None = None
    last_name: str | None = None
    addresses: list[Address] = []

    class Config:
        from_attributes = True