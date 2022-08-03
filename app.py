from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
import fastapi.security as _security
import sqlalchemy.orm as _orm

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


@app.patch("/api/users/change-password")
async def change_password(
        new_pass_data: _User_schema.ChangePassword,
        user: _User_schema.User = Depends(_User_service.get_current_user),
        db: _orm.Session = Depends(_db.get_db)):
    # Authenticate user
    db_user = await _User_service.authenticate_user(
        db=db,
        username=user.username,
        password=new_pass_data.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.")

    # Change password
    await _User_service.change_password(db=db, new_pass_data=new_pass_data, user_model=db_user)

    # Return something.
    return {
        "message": "Your password has been changed."
    }


@app.get("/api/users", response_model=_User_schema.User)
async def get_user(
        user: _User_schema.User = Depends(_User_service.get_current_user)):
    print(f"user: {user}")
    return user


@app.post("/api/goals", response_model=_Goal_schema.Goal)
async def create_goal(
        goal: _Goal_schema.GoalCreate,
        user: _User_schema.User = Depends(_User_service.get_current_user),
        db: _orm.Session = Depends(_db.get_db)
):
    goal = await _Goal_service.create_goal(db=db, user=user, goal=goal)
    return goal


@app.get("/api/goals", response_model=List[_Goal_schema.Goal])
async def view_all_goals_from_user(
        user: _User_schema.User = Depends(_User_service.get_current_user),
        db: _orm.Session = Depends(_db.get_db)
):
    return await _Goal_service.view_all_goals_from_user(db=db, user=user)


@app.get("/api/goals/{goal_id}", response_model=_Goal_schema.Goal)
async def view_goal_by_id(
        goal_id: int,
        user: _User_schema.User = Depends(_User_service.get_current_user),
        db: _orm.Session = Depends(_db.get_db)
):
    goal = await _Goal_service.view_goal_by_id(db=db, goal_id=goal_id, user=user)

    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Goal not found.")

    return goal


@app.patch("/api/goals/{goal_id}", response_model=_Goal_schema.Goal)
async def update_goal(
        goal_id: int,
        goal_data: _Goal_schema.GoalCreate,
        user: _User_schema.User = Depends(_User_service.get_current_user),
        db: _orm.Session = Depends(_db.get_db)
):
    pass
