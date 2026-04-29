from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import StudentSkill
from app.schemas.common import AdmissionOut, FeePlanOut, StudentProfileOut, UserOut


class AdminCreateStudentRequest(BaseModel):
    email: str = Field(description="Student email address used for student login.")
    full_name: str = Field(description="Student full name.")
    password: str = Field(min_length=6, description="Initial student password with at least 6 characters.")
    phone: str | None = Field(default=None, description="Student phone number.")
    address: str | None = Field(default=None, description="Student address.")
    guardian_name: str | None = Field(default=None, description="Guardian or parent name.")
    guardian_phone: str | None = Field(default=None, description="Guardian or parent phone number.")
    skills: list[StudentSkill] = Field(
        default_factory=list,
        description="Cricket skills selected for the student. Allowed values: Batting, Bowling, Wicket Keeping.",
    )
    total_fee: Decimal = Field(gt=0, description="Total fee assigned to the student.")
    currency: str = Field(default="INR", description="Fee currency, for example INR.")


class AdminStudentResponse(BaseModel):
    user: UserOut
    profile: StudentProfileOut
    admission: AdmissionOut
    fee_plan: FeePlanOut


class AdminUpdateStudentRequest(BaseModel):
    email: str | None = Field(default=None, description="Updated student email address used for login.")
    full_name: str | None = Field(default=None, description="Updated student full name.")
    password: str | None = Field(default=None, min_length=6, description="Updated student password.")
    phone: str | None = Field(default=None, description="Updated student phone number.")
    address: str | None = Field(default=None, description="Updated student address.")
    guardian_name: str | None = Field(default=None, description="Updated guardian or parent name.")
    guardian_phone: str | None = Field(default=None, description="Updated guardian or parent phone number.")
    skills: list[StudentSkill] | None = Field(
        default=None,
        description="Updated cricket skills. Allowed values: Batting, Bowling, Wicket Keeping.",
    )
    total_fee: Decimal | None = Field(default=None, gt=0, description="Updated total fee assigned to the student.")
    currency: str | None = Field(default=None, description="Updated fee currency, for example INR.")


class AdminAdmitStudentRequest(BaseModel):
    remarks: str | None = Field(default=None, description="Optional admission remark recorded by the admin.")


class PaymentNotificationItem(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    student_email: str
    claimed_amount: Decimal
    payment_date: date
    payment_mode: str
    reference_no: str | None = None
    note: str | None = None
    status: str
    created_at: datetime


class AdminApproveNotificationRequest(BaseModel):
    approved_amount: Decimal | None = Field(default=None, gt=0)
    paid_on: date | None = None
    note: str | None = None
    admin_remark: str | None = None


class AdminRejectNotificationRequest(BaseModel):
    admin_remark: str = Field(min_length=2)


class ManualPaymentRequest(BaseModel):
    student_id: UUID
    amount: Decimal = Field(gt=0)
    paid_on: date
    mode: str = Field(min_length=2)
    reference_no: str | None = None
    note: str | None = None


class AdminPaymentHistoryItem(BaseModel):
    id: UUID
    amount: Decimal
    paid_on: date
    mode: str
    source: str
    reference_no: str | None = None
    note: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminStudentPaymentHistoryResponse(BaseModel):
    payment_status: str
    total_approved_amount: Decimal
    fee_plan: FeePlanOut | None = None
    payments: list[AdminPaymentHistoryItem]
