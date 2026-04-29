from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_student
from app.core.database import get_db
from app.models.user import User
from app.schemas.student import (
    StudentAdmissionResponse,
    StudentMeResponse,
    StudentPaymentNotificationCreate,
    StudentPaymentNotificationResponse,
    StudentPaymentsResponse,
)
from app.services.student_service import StudentService

router = APIRouter(prefix="/student", tags=["Student"])


@router.get(
    "/me",
    response_model=StudentMeResponse,
    summary="Get student profile",
    description="Return the authenticated student's user account and profile information.",
)
async def me(student: User = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await StudentService(db).get_student_overview(student)


@router.get(
    "/admission",
    response_model=StudentAdmissionResponse,
    summary="Get admission status",
    description="Return admission status, fee plan, and derived payment status for the authenticated student.",
)
async def admission(student: User = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await StudentService(db).get_admission_status(student.id)


@router.get(
    "/payments",
    response_model=StudentPaymentsResponse,
    summary="Get payment summary",
    description="Return approved payments, total approved amount, fee plan, and derived payment status.",
)
async def payments(student: User = Depends(get_current_student), db: AsyncSession = Depends(get_db)):
    return await StudentService(db).get_payments(student.id)


@router.post(
    "/payment-notification",
    response_model=StudentPaymentNotificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit payment notification",
    description="Allow an admitted student to submit an offline payment notification for admin review.",
)
async def payment_notification(
    payload: StudentPaymentNotificationCreate,
    student: User = Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    return await StudentService(db).create_payment_notification(student, payload)
