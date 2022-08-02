from typing import TYPE_CHECKING
from fastapi import FastAPI, Depends, HTTPException, status
import fastapi.security as _security
import sqlalchemy.orm as _orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from schemas import User as _User_schema
from schemas import Goal as _Goal_schema
from controllers import database as _db
from controllers import UserService as _User_service
from controllers import GoalService as _Goal_service

app = FastAPI()


# Post all your routes here
@app.get("/")
def index() -> str:
    return "Goals App: Create your #goals here!"


@app.post("/api/users", response_model=_User_schema.User)
async def register_user(user: _User_schema.UserCreate, db: _orm.Session = Depends(_db.get_db)):
    # Check if one of the fields are blank
    if (
            user.email == "" or
            user.username == "" or
            user.password == ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email, username or password must not be blank.")

    # Check if email is valid
    is_email_valid = _User_service.is_email_valid(user.email)
    if not is_email_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not valid.")

    # Check if there are any duplicate usernames/emails
    is_there_duplicates = _User_service.check_for_duplicates(db=db, username=user.username, email=user.email)
    if is_there_duplicates:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email and/or username is taken. Please enter different credentials.")

    user = await _User_service.register_user(db=db, user=user)

    return user


@app.post("/api/users/login")
async def user_login(
        user_data: _security.OAuth2PasswordRequestForm = Depends(),
        db: _orm.Session = Depends(_db.get_db)):
    user = await _User_service.authenticate_user(
        db=db,
        username=user_data.username,
        password=user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.")

    return await _User_service.create_token(user=user)
