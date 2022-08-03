import sqlalchemy.orm as _orm
import fastapi.security as _security
from typing import List

from controllers import database as _db
from models import Goal as _Goal_model
from schemas import Goal as _Goal_schema
from models import User as _User_model
from schemas import User as _User_schema

oauth2schema = _security.OAuth2PasswordBearer("/api/users/login")


async def create_goal(
        db: _orm.Session,
        user: _User_schema.User,
        goal: _Goal_schema.GoalCreate
) -> _Goal_schema.Goal:
    goal = _Goal_model.GoalModel(**goal.dict(), user_id=user.id)
    _db.add_to_db(db=db, model=goal)

    return _Goal_schema.Goal.from_orm(goal)


async def view_all_goals_from_user(
        db: _orm.Session,
        user: _User_schema.User
) -> List[_Goal_schema.Goal]:
    goals = db.query(_Goal_model.GoalModel).filter_by(user_id=user.id)

    return list(map(_Goal_schema.Goal.from_orm, goals))


async def view_goal_by_id(
        db: _orm.Session,
        goal_id: int,
        user: _User_schema.User
):
    goal = db.query(_Goal_model.GoalModel).filter_by(id=goal_id, user_id=user.id).first()

    return goal


async def update_goal(
        db: _orm.Session,
        new_goal_data: _Goal_schema.GoalCreate,
        goal_model: _Goal_model.GoalModel
) -> _Goal_schema.Goal:
    goal_model.title = new_goal_data.title
    goal_model.description = new_goal_data.description
    goal_model.priority = new_goal_data.priority

    _db.commit_to_db(db=db, model=goal_model)

    return _Goal_schema.Goal.from_orm(goal_model)
