"""initial migration

Revision ID: 7f047fc98559
Revises: 
Create Date: 2022-08-01 16:33:42.006090

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.orm as orm
from datetime import datetime as _dt


# revision identifiers, used by Alembic.
revision = '7f047fc98559'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(100), index=True, unique=True, nullable=False),
        sa.Column("email", sa.String(100), index=True, unique=True, nullable=False),
        sa.Column("password", sa.String(200), nullable=False),
        sa.Column("is_email_verified", sa.Boolean, default=False),
        sa.Column("date_created", sa.DateTime, default=_dt.utcnow),
        sa.Column("date_updated", sa.DateTime, default=_dt.utcnow),

        orm.relationship("GoalModel", back_populates="user"),
    )
    op.create_table(
        "goals",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("title", sa.String(100), index=True, nullable=False),
        sa.Column("description", sa.Text),
        sa.Column("priority", sa.String(100), nullable=False),
        sa.Column("date_started", sa.DateTime, default=_dt.utcnow),
        sa.Column("date_ended", sa.DateTime),
        sa.Column("is_finished", sa.Boolean, default=False),
        sa.Column("date_created", sa.DateTime, default=_dt.utcnow),
        sa.Column("date_updated", sa.DateTime, default=_dt.utcnow),

        orm.relationship("UserModel", back_populates="goals"),
    )


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("goals")
