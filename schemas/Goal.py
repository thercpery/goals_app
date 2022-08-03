from datetime import datetime as _dt
import pydantic as _pydantic


class _GoalBase(_pydantic.BaseModel):
    title: str
    description: str
    priority: str


class GoalCreate(_GoalBase):
    pass


class Goal(_GoalBase):
    id: int
    user_id: int
    date_started: _dt
    is_finished: bool
    date_created: _dt
    date_updated: _dt

    class Config:
        orm_mode = True


class FinishedGoal(Goal):
    date_ended: _dt

    class Config:
        orm_mode = True
