from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import get_password_hash
from app.models.admission import Admission
from app.models.enums import AdmissionStatus, NotificationStatus, PaymentSource, UserRole
from app.models.fee_plan import FeePlan
from app.models.payment import Payment
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.user_repository import UserRepository
from app.schemas.admin import (
    AdminApproveNotificationRequest,
    AdminCreateStudentRequest,
    AdminUpdateStudentRequest,
    ManualPaymentRequest,
)
from app.services.student_service import derive_payment_status


class AdminService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.student_repo = StudentRepository(db)
        self.notification_repo = NotificationRepository(db)
        self.payment_repo = PaymentRepository(db)

    async def create_student(self, payload: AdminCreateStudentRequest) -> dict:
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student email already exists")

        student_user = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            role=UserRole.student,
            is_active=True,
        )
        self.user_repo.add(student_user)
        await self.db.flush()

        profile = StudentProfile(
            user_id=student_user.id,
            phone=payload.phone,
            address=payload.address,
            guardian_name=payload.guardian_name,
            guardian_phone=payload.guardian_phone,
            skills=[skill.value for skill in payload.skills],
        )
        admission = Admission(student_id=student_user.id, status=AdmissionStatus.pending)
        fee_plan = FeePlan(student_id=student_user.id, total_fee=payload.total_fee, currency=payload.currency)

        self.student_repo.add_profile(profile)
        self.student_repo.add_admission(admission)
        self.student_repo.add_or_update_fee_plan(fee_plan)

        await self.db.commit()
        await self.db.refresh(student_user)
        await self.db.refresh(profile)
        await self.db.refresh(admission)
        await self.db.refresh(fee_plan)

        return {
            "user": student_user,
            "profile": profile,
            "admission": admission,
            "fee_plan": fee_plan,
        }

    async def update_student(self, student_id: UUID, payload: AdminUpdateStudentRequest) -> dict:
        student = await self.user_repo.get_by_id(student_id)
        if not student or student.role != UserRole.student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        if payload.email and payload.email != student.email:
            existing = await self.user_repo.get_by_email(payload.email)
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Student email already exists")
            student.email = payload.email

        if payload.full_name is not None:
            student.full_name = payload.full_name
        if payload.password is not None:
            student.hashed_password = get_password_hash(payload.password)

        profile = await self.student_repo.get_profile(student_id)
        if not profile:
            profile = StudentProfile(user_id=student_id, skills=[])
            self.student_repo.add_profile(profile)

        if payload.phone is not None:
            profile.phone = payload.phone
        if payload.address is not None:
            profile.address = payload.address
        if payload.guardian_name is not None:
            profile.guardian_name = payload.guardian_name
        if payload.guardian_phone is not None:
            profile.guardian_phone = payload.guardian_phone
        if payload.skills is not None:
            profile.skills = [skill.value for skill in payload.skills]

        admission = await self.student_repo.get_admission(student_id)
        if not admission:
            admission = Admission(student_id=student_id, status=AdmissionStatus.pending)
            self.student_repo.add_admission(admission)

        fee_plan = await self.student_repo.get_fee_plan(student_id)
        if not fee_plan and payload.currency is not None and payload.total_fee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="total_fee is required when creating a missing fee plan",
            )

        if not fee_plan and payload.total_fee is not None:
            fee_plan = FeePlan(
                student_id=student_id,
                total_fee=payload.total_fee,
                currency=payload.currency or "INR",
            )
            self.student_repo.add_or_update_fee_plan(fee_plan)

        if fee_plan:
            if payload.total_fee is not None:
                fee_plan.total_fee = payload.total_fee
            if payload.currency is not None:
                fee_plan.currency = payload.currency

        await self.db.commit()
        await self.db.refresh(student)
        await self.db.refresh(profile)
        await self.db.refresh(admission)
        if fee_plan:
            await self.db.refresh(fee_plan)

        return {
            "user": student,
            "profile": profile,
            "admission": admission,
            "fee_plan": fee_plan,
        }

    async def admit_student(self, student_id: UUID, admin_id: UUID, remarks: str | None) -> Admission:
        student = await self.user_repo.get_by_id(student_id)
        if not student or student.role != UserRole.student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        admission = await self.student_repo.get_admission(student_id)
        if not admission:
            admission = Admission(student_id=student_id)
            self.student_repo.add_admission(admission)

        admission.status = AdmissionStatus.admitted
        admission.admitted_at = datetime.now(UTC)
        admission.admitted_by = admin_id
        admission.remarks = remarks

        await self.db.commit()
        await self.db.refresh(admission)
        return admission

    async def list_students(self) -> list[User]:
        return await self.user_repo.list_students()

    async def delete_student(self, student_id: UUID) -> None:
        student = await self.user_repo.get_by_id(student_id)
        if not student or student.role != UserRole.student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        await self.payment_repo.delete_by_student(student_id)
        await self.notification_repo.delete_by_student(student_id)

        profile = await self.student_repo.get_profile(student_id)
        if profile:
            await self.student_repo.delete_profile(profile)

        admission = await self.student_repo.get_admission(student_id)
        if admission:
            await self.student_repo.delete_admission(admission)

        fee_plan = await self.student_repo.get_fee_plan(student_id)
        if fee_plan:
            await self.student_repo.delete_fee_plan(fee_plan)

        await self.user_repo.delete(student)
        await self.db.commit()

    async def list_payment_notifications(self):
        notifications = await self.notification_repo.list_all()
        items = []
        for row in notifications:
            student = await self.user_repo.get_by_id(row.student_id)
            if not student:
                continue
            items.append(
                {
                    "id": row.id,
                    "student_id": row.student_id,
                    "student_name": student.full_name,
                    "student_email": student.email,
                    "claimed_amount": row.claimed_amount,
                    "payment_date": row.payment_date,
                    "payment_mode": row.payment_mode,
                    "reference_no": row.reference_no,
                    "note": row.note,
                    "status": row.status,
                    "created_at": row.created_at,
                }
            )
        return items

    async def approve_notification(
        self, notification_id: UUID, admin_id: UUID, payload: AdminApproveNotificationRequest
    ) -> Payment:
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notification.status != NotificationStatus.pending:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Notification already reviewed")

        approved_amount = payload.approved_amount or Decimal(notification.claimed_amount)
        payment = Payment(
            student_id=notification.student_id,
            amount=approved_amount,
            paid_on=payload.paid_on or notification.payment_date,
            mode=notification.payment_mode,
            reference_no=notification.reference_no,
            note=payload.note or notification.note,
            source=PaymentSource.notification,
            notification_id=notification.id,
            created_by=admin_id,
        )
        self.payment_repo.add(payment)

        notification.status = NotificationStatus.approved
        notification.reviewed_by = admin_id
        notification.reviewed_at = datetime.now(UTC)
        notification.admin_remark = payload.admin_remark

        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def reject_notification(self, notification_id: UUID, admin_id: UUID, admin_remark: str):
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        if notification.status != NotificationStatus.pending:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Notification already reviewed")

        notification.status = NotificationStatus.rejected
        notification.reviewed_by = admin_id
        notification.reviewed_at = datetime.now(UTC)
        notification.admin_remark = admin_remark
        await self.db.commit()

    async def add_manual_payment(self, payload: ManualPaymentRequest, admin_id: UUID) -> Payment:
        student = await self.user_repo.get_by_id(payload.student_id)
        if not student or student.role != UserRole.student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        payment = Payment(
            student_id=payload.student_id,
            amount=payload.amount,
            paid_on=payload.paid_on,
            mode=payload.mode,
            reference_no=payload.reference_no,
            note=payload.note,
            source=PaymentSource.manual,
            notification_id=None,
            created_by=admin_id,
        )
        self.payment_repo.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_student_payment_history(self, student_id: UUID) -> dict:
        student = await self.user_repo.get_by_id(student_id)
        if not student or student.role != UserRole.student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

        fee_plan = await self.student_repo.get_fee_plan(student_id)
        payments = await self.payment_repo.list_by_student(student_id)
        total_paid = await self.payment_repo.total_paid_by_student(student_id)
        status_value = derive_payment_status(total_paid, fee_plan.total_fee if fee_plan else None)

        return {
            "payment_status": status_value.value,
            "total_approved_amount": total_paid,
            "fee_plan": fee_plan,
            "payments": payments,
        }
