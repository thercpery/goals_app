import pydantic as _pydantic
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from middleware import database as _db


def get_db():
    db = _db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_to_db(db: "Session", model: _pydantic.BaseModel) -> None:
    db.add(model)
    db.commit()
    db.refresh(model)


def commit_to_db(db: "Session", model: _pydantic.BaseModel) -> None:
    db.commit()
    db.refresh(model)
