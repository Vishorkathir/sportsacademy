import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import AdmissionStatus


class Admission(Base):
    __tablename__ = "admissions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    status: Mapped[AdmissionStatus] = mapped_column(
        Enum(AdmissionStatus, name="admission_status"), default=AdmissionStatus.pending, nullable=False
    )
    admitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    admitted_by: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))

    student = relationship("User", back_populates="admission", foreign_keys=[student_id])
