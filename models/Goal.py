from datetime import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import middleware.database as _database


class GoalModel(_database.Base):
    __tablename__ = "goals"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    title = _sql.Column(_sql.String(100), nullable=False, index=True)
    description = _sql.Column(_sql.Text)
    priority = _sql.Column(_sql.String(100), nullable=False)
    date_started = _sql.Column(_sql.DateTime, default=_dt.utcnow)
    date_ended = _sql.Column(_sql.DateTime)
    is_finished = _sql.Column(_sql.Boolean, default=False)
    date_created = _sql.Column(_sql.DateTime, default=_dt.utcnow)
    date_updated = _sql.Column(_sql.DateTime, default=_dt.utcnow)

    owner = _orm.relationship("UserModel", back_populates="users")
