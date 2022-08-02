from typing import TYPE_CHECKING
from fastapi import FastAPI, Depends, HTTPException, status
import sqlalchemy.orm as _orm

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

from schemas import User as _user_schema
from schemas import Goal as _goal_schema
from controllers import database as _db
from controllers import UserService as _user_service
from controllers import GoalService as _goal_service

app = FastAPI()


# Post all your routes here
@app.get("/")
def index() -> str:
    return "Goals App: Create your #goals here!"


@app.post("/api/users", response_model=_user_schema.User)
async def register_user(user: _user_schema.UserCreate, db: _orm.Session = Depends(_db.get_db)):
    # Check if email is valid
    is_email_valid = _user_service.is_email_valid(user.email)
    if not is_email_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email not valid.")

    # Check if there are any duplicate usernames/emails
    is_there_duplicates = _user_service.check_for_duplicates(db=db, username=user.username, email=user.email)
    if is_there_duplicates:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email and/or username is taken. Please enter different credential")

    user = await _user_service.register_user(db=db, user=user)

    return user

