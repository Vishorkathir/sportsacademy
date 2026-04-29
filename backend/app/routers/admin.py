from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_admin
from app.core.database import get_db
from app.models.user import User
from app.schemas.admin import (
    AdminAdmitStudentRequest,
    AdminApproveNotificationRequest,
    AdminCreateStudentRequest,
    AdminPaymentHistoryItem,
    AdminStudentPaymentHistoryResponse,
    AdminRejectNotificationRequest,
    AdminStudentResponse,
    AdminUpdateStudentRequest,
    ManualPaymentRequest,
    PaymentNotificationItem,
)
from app.schemas.common import AdmissionOut, UserOut
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post(
    "/students",
    response_model=AdminStudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a student account",
    description="Create a student user, profile, pending admission record, and fee plan in one request.",
)
async def create_student(
    payload: AdminCreateStudentRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return await AdminService(db).create_student(payload)


@router.patch(
    "/students/{student_id}",
    response_model=AdminStudentResponse,
    summary="Update a student account",
    description="Update student login info, profile fields, skills, and fee plan details.",
)
async def update_student(
    student_id: UUID,
    payload: AdminUpdateStudentRequest,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return await AdminService(db).update_student(student_id, payload)


@router.post(
    "/admit/{student_id}",
    response_model=AdmissionOut,
    summary="Admit a student",
    description="Mark a student as admitted so they can start submitting payment notifications.",
)
async def admit_student(
    student_id: UUID,
    payload: AdminAdmitStudentRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return await AdminService(db).admit_student(student_id, admin.id, payload.remarks)


@router.get(
    "/students",
    response_model=list[UserOut],
    summary="List students",
    description="Return all student user accounts ordered by newest first.",
)
async def list_students(db: AsyncSession = Depends(get_db), _: User = Depends(get_current_admin)):
    return await AdminService(db).list_students()


@router.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student account",
    description="Delete the student and all profile, admission, notification, payment, and fee plan data linked to that student.",
)
async def delete_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    await AdminService(db).delete_student(student_id)


@router.get(
    "/payment-notifications",
    response_model=list[PaymentNotificationItem],
    summary="List payment notifications",
    description="Return all submitted student payment notifications for admin review.",
)
async def list_payment_notifications(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return await AdminService(db).list_payment_notifications()


@router.post(
    "/payment-notifications/{id}/approve",
    response_model=AdminPaymentHistoryItem,
    summary="Approve a payment notification",
    description="Approve a pending student payment notification and create an official payment record.",
)
async def approve_notification(
    id: UUID,
    payload: AdminApproveNotificationRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return await AdminService(db).approve_notification(id, admin.id, payload)


@router.post(
    "/payment-notifications/{id}/reject",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Reject a payment notification",
    description="Reject a pending student payment notification without creating a payment record.",
)
async def reject_notification(
    id: UUID,
    payload: AdminRejectNotificationRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    await AdminService(db).reject_notification(id, admin.id, payload.admin_remark)


@router.post(
    "/payments/manual",
    response_model=AdminPaymentHistoryItem,
    status_code=status.HTTP_201_CREATED,
    summary="Record a manual payment",
    description="Create an official payment directly without going through a student notification.",
)
async def manual_payment(
    payload: ManualPaymentRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    return await AdminService(db).add_manual_payment(payload, admin.id)


@router.get(
    "/students/{student_id}/payments",
    response_model=AdminStudentPaymentHistoryResponse,
    summary="Get student payment history",
    description="Return the student's approved payment summary, fee plan, and payment history.",
)
async def student_payment_history(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    return await AdminService(db).get_student_payment_history(student_id)
