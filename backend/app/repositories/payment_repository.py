from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def add(self, payment: Payment) -> Payment:
        self.db.add(payment)
        return payment

    async def list_by_student(self, student_id: UUID) -> list[Payment]:
        stmt = select(Payment).where(Payment.student_id == student_id).order_by(Payment.paid_on.desc(), Payment.created_at.desc())
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def delete_by_student(self, student_id: UUID) -> None:
        payments = await self.list_by_student(student_id)
        for payment in payments:
            await self.db.delete(payment)

    async def total_paid_by_student(self, student_id: UUID) -> Decimal:
        stmt = select(func.coalesce(func.sum(Payment.amount), 0)).where(Payment.student_id == student_id)
        total = await self.db.scalar(stmt)
        return Decimal(total)
