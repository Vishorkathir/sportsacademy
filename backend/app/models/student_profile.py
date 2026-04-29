import uuid

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    guardian_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    guardian_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    skills: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    student = relationship("User", back_populates="student_profile")
