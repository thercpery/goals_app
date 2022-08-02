from datetime import datetime as _dt
from typing import List
import pydantic as _pydantic
from schemas.Goal import Goal


class _UserBase(_pydantic.BaseModel):
    username: str
    email: str


class UserCreate(_UserBase):
    password: str


class User(_UserBase):
    id: int
    is_email_verified: bool
    date_created: _dt
    date_updated: _dt
    goals: List[Goal] = []

    class Config:
        orm_mode = True
