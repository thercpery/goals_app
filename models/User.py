from datetime import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import middleware.database as _database


class UserModel(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String(100), index=True, unique=True, nullable=False)
    email = _sql.Column(_sql.String(100), index=True, unique=True, nullable=False)
    password = _sql.Column(_sql.String(200), nullable=False)
    is_email_verified = _sql.Column(_sql.Boolean, default=False)
    date_created = _sql.Column(_sql.DateTime, default=_dt.utcnow)
    date_updated = _sql.Column(_sql.DateTime, default=_dt.utcnow)

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.password)
