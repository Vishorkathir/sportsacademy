from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import AdmissionStatus, DerivedPaymentStatus, NotificationStatus
from app.models.payment_notification import PaymentNotification
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentPaymentNotificationCreate


def derive_payment_status(total_paid: Decimal, total_fee: Decimal | None) -> DerivedPaymentStatus:
    if total_paid <= 0:
        return DerivedPaymentStatus.nopaid
    if total_fee is None:
        return DerivedPaymentStatus.halfpayed
    if total_paid < total_fee:
        return DerivedPaymentStatus.halfpayed
    return DerivedPaymentStatus.fulpayed


class StudentService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.student_repo = StudentRepository(db)
        self.payment_repo = PaymentRepository(db)
        self.notification_repo = NotificationRepository(db)

    async def get_student_overview(self, user: User) -> dict:
        profile = await self.student_repo.get_profile(user.id)
        return {"user": user, "profile": profile}

    async def get_admission_status(self, student_id) -> dict:
        admission = await self.student_repo.get_admission(student_id)
        fee_plan = await self.student_repo.get_fee_plan(student_id)
        total_paid = await self.payment_repo.total_paid_by_student(student_id)
        payment_status = derive_payment_status(total_paid, fee_plan.total_fee if fee_plan else None)
        return {
            "admission": admission,
            "fee_plan": fee_plan,
            "total_approved_amount": total_paid,
            "payment_status": payment_status.value,
        }

    async def get_payments(self, student_id) -> dict:
        payments = await self.payment_repo.list_by_student(student_id)
        fee_plan = await self.student_repo.get_fee_plan(student_id)
        total_paid = await self.payment_repo.total_paid_by_student(student_id)
        payment_status = derive_payment_status(total_paid, fee_plan.total_fee if fee_plan else None)

        return {
            "payments": payments,
            "fee_plan": fee_plan,
            "total_approved_amount": total_paid,
            "payment_status": payment_status.value,
        }

    async def create_payment_notification(self, student: User, payload: StudentPaymentNotificationCreate) -> PaymentNotification:
        admission = await self.student_repo.get_admission(student.id)
        if not admission or admission.status != AdmissionStatus.admitted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is not admitted yet. Payment notification cannot be submitted.",
            )

        notification = PaymentNotification(
            student_id=student.id,
            claimed_amount=payload.claimed_amount,
            payment_date=payload.payment_date,
            payment_mode=payload.payment_mode,
            reference_no=payload.reference_no,
            note=payload.note,
            status=NotificationStatus.pending,
        )
        self.notification_repo.add(notification)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
