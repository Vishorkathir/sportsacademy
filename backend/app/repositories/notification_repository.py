from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment_notification import PaymentNotification


class NotificationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    def add(self, notification: PaymentNotification) -> PaymentNotification:
        self.db.add(notification)
        return notification

    async def get_by_id(self, notification_id: UUID) -> PaymentNotification | None:
        return await self.db.scalar(select(PaymentNotification).where(PaymentNotification.id == notification_id))

    async def list_all(self) -> list[PaymentNotification]:
        stmt = select(PaymentNotification).order_by(PaymentNotification.created_at.desc())
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def list_by_student(self, student_id: UUID) -> list[PaymentNotification]:
        stmt = select(PaymentNotification).where(PaymentNotification.student_id == student_id).order_by(PaymentNotification.created_at.desc())
        result = await self.db.scalars(stmt)
        return list(result.all())

    async def delete_by_student(self, student_id: UUID) -> None:
        notifications = await self.list_by_student(student_id)
        for notification in notifications:
            await self.db.delete(notification)
