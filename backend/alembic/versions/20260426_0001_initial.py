"""initial admission and payment schema

Revision ID: 20260426_0001
Revises:
Create Date: 2026-04-26 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20260426_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_role = sa.Enum("admin", "student", name="user_role")
    admission_status = sa.Enum("pending", "admitted", "rejected", name="admission_status")
    notification_status = sa.Enum("pending", "approved", "rejected", name="notification_status")
    payment_source = sa.Enum("manual", "notification", name="payment_source")

    bind = op.get_bind()
    user_role.create(bind, checkfirst=True)
    admission_status.create(bind, checkfirst=True)
    notification_status.create(bind, checkfirst=True)
    payment_source.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "student_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("guardian_name", sa.String(length=255), nullable=True),
        sa.Column("guardian_phone", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("user_id"),
    )

    op.create_table(
        "admissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", admission_status, nullable=False, server_default="pending"),
        sa.Column("admitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("admitted_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("remarks", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["admitted_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("student_id"),
    )

    op.create_table(
        "fee_plans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("total_fee", sa.Numeric(12, 2), nullable=False),
        sa.Column("currency", sa.String(length=10), nullable=False, server_default="INR"),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("student_id"),
    )

    op.create_table(
        "payment_notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("claimed_amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("payment_date", sa.Date(), nullable=False),
        sa.Column("payment_mode", sa.String(length=50), nullable=False),
        sa.Column("reference_no", sa.String(length=100), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("status", notification_status, nullable=False, server_default="pending"),
        sa.Column("admin_remark", sa.Text(), nullable=True),
        sa.Column("reviewed_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["reviewed_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
    )

    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("paid_on", sa.Date(), nullable=False),
        sa.Column("mode", sa.String(length=50), nullable=False),
        sa.Column("reference_no", sa.String(length=100), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("source", payment_source, nullable=False),
        sa.Column("notification_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["notification_id"], ["payment_notifications.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["student_id"], ["users.id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("payments")
    op.drop_table("payment_notifications")
    op.drop_table("fee_plans")
    op.drop_table("admissions")
    op.drop_table("student_profiles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    sa.Enum(name="payment_source").drop(bind, checkfirst=True)
    sa.Enum(name="notification_status").drop(bind, checkfirst=True)
    sa.Enum(name="admission_status").drop(bind, checkfirst=True)
    sa.Enum(name="user_role").drop(bind, checkfirst=True)
