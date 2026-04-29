from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import StudentSkill


class UserOut(BaseModel):
    id: UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentProfileOut(BaseModel):
    phone: str | None = None
    address: str | None = None
    guardian_name: str | None = None
    guardian_phone: str | None = None
    skills: list[StudentSkill] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class AdmissionOut(BaseModel):
    status: str
    admitted_at: datetime | None = None
    remarks: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FeePlanOut(BaseModel):
    total_fee: Decimal
    currency: str
    effective_from: date

    model_config = ConfigDict(from_attributes=True)


class PaymentOut(BaseModel):
    id: UUID
    amount: Decimal
    paid_on: date
    mode: str
    reference_no: str | None = None
    note: str | None = None
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
