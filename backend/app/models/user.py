import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    student_profile = relationship("StudentProfile", back_populates="student", uselist=False)
    admission = relationship("Admission", back_populates="student", uselist=False, foreign_keys="Admission.student_id")
    fee_plan = relationship("FeePlan", back_populates="student", uselist=False)
    payment_notifications = relationship("PaymentNotification", back_populates="student", foreign_keys="PaymentNotification.student_id")
    payments = relationship("Payment", back_populates="student", foreign_keys="Payment.student_id")
