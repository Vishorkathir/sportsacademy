"""add skills to student profiles

Revision ID: 20260426_0002
Revises: 20260426_0001
Create Date: 2026-04-26 00:30:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "20260426_0002"
down_revision = "20260426_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "student_profiles",
        sa.Column("skills", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.alter_column("student_profiles", "skills", server_default=None)


def downgrade() -> None:
    op.drop_column("student_profiles", "skills")
