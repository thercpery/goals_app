from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import email_validator as _email_check
import passlib.hash as _hash

from controllers import database as _db
from models import User as _user_model
from schemas import User as _user_schemas


def check_for_duplicates(db: "Session", username: str, email: str) -> bool:
    db_email = db.query(_user_model.UserModel).filter(_user_model.UserModel.email == email).first()
    db_username = db.query(_user_model.UserModel).filter(_user_model.UserModel.username == username).first()

    if (db_email is not None) or (db_username is not None):
        return True

    return False


def is_email_valid(email: str) -> bool:
    try:
        _email_check.validate_email(email)
        return True
    except _email_check.EmailSyntaxError:
        return False


async def verify_email(db: "Session", email: str) -> bool:
    db_user = db.query(_user_model.UserModel).filter(_user_model.UserModel.email == email).first()

    if not db_user:
        return False
    return True


async def register_user(db: "Session", user: _user_schemas.UserCreate) -> _user_schemas.User:
    hash_password = _hash.bcrypt.hash(user.password)
    user_obj = _user_model.UserModel(username=user.username, email=user.email, password=hash_password)

    _db.add_to_db(db=db, model=user_obj)
    return user_obj
