from typing import TYPE_CHECKING
import sqlalchemy.orm as _orm
if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import email_validator as _email_check
import passlib.hash as _hash
import fastapi.security as _security
from dotenv import load_dotenv
import jwt as _jwt
import os as _os


from controllers import database as _db
from models import User as _User_model
from schemas import User as _User_schemas

load_dotenv(".env")
JWT_SECRET_KEY = _os.environ.get("JWT_SECRET_KEY")
oauth2schema =_security.OAuth2PasswordBearer("/api/users/login")


def check_for_duplicates(db: "Session", username: str, email: str) -> bool:
    db_email = db.query(_User_model.UserModel).filter(_User_model.UserModel.email == email).first()
    db_username = db.query(_User_model.UserModel).filter(_User_model.UserModel.username == username).first()

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
    db_user = db.query(_User_model.UserModel).filter(_User_model.UserModel.email == email).first()

    if not db_user:
        return False
    return True


async def verify_username(db: "Session", username: str) -> bool:
    db_user = db.query(_User_model.UserModel).filter(_User_model.UserModel.username == username).first()

    if not db_user:
        return False
    return True


async def get_user_by_username(db: "Session", username: str):
    return db.query(_User_model.UserModel).filter(_User_model.UserModel.username == username).first()


# Put all callback functions associated with routes ("/api/users") here.
async def register_user(db: "Session", user: _User_schemas.UserCreate) -> _User_schemas.User:
    hash_password = _hash.bcrypt.hash(user.password)
    user_obj = _User_model.UserModel(username=user.username, email=user.email, password=hash_password)

    _db.add_to_db(db=db, model=user_obj)
    return user_obj


async def authenticate_user(db: "Session", username: str, password: str):
    user = await get_user_by_username(db=db, username=username)

    if not user:
        return False
    if not user.verify_password(password=password):
        return False

    return user


async def create_token(user: _User_model.UserModel) -> dict:
    user_schema_obj = _User_schemas.User.from_orm(user)
    user_dict = user_schema_obj.dict()
    del user_dict["date_created"]
    del user_dict["date_updated"]

    token = _jwt.encode(user_dict, JWT_SECRET_KEY)

    return dict(access_token=token, token_type="bearer")

