from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import AdmissionOut, FeePlanOut, PaymentOut, StudentProfileOut, UserOut


class StudentMeResponse(BaseModel):
    user: UserOut
    profile: StudentProfileOut | None = None


class StudentAdmissionResponse(BaseModel):
    admission: AdmissionOut | None = None
    fee_plan: FeePlanOut | None = None
    total_approved_amount: Decimal
    payment_status: str


class StudentPaymentsResponse(BaseModel):
    payment_status: str
    total_approved_amount: Decimal
    fee_plan: FeePlanOut | None = None
    payments: list[PaymentOut]


class StudentPaymentNotificationCreate(BaseModel):
    claimed_amount: Decimal = Field(gt=0, description="Amount the student claims to have paid.")
    payment_date: date = Field(description="Date on which the payment was made.")
    payment_mode: str = Field(min_length=2, description="Payment mode such as cash, bank_transfer, or UPI.")
    reference_no: str | None = Field(default=None, description="Optional bank reference or transaction number.")
    note: str | None = Field(default=None, description="Optional note from the student.")


class StudentPaymentNotificationResponse(BaseModel):
    id: UUID
    claimed_amount: Decimal
    payment_date: date
    payment_mode: str
    reference_no: str | None = None
    note: str | None = None
    status: str
    created_at: datetime
