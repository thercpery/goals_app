"""drop is email verified column

Revision ID: 7de7478b7256
Revises: 7f047fc98559
Create Date: 2022-08-02 16:18:24.109116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7de7478b7256'
down_revision = '7f047fc98559'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("users", "is_email_verified")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_email_verified", sa.Boolean, default=False),
    )
