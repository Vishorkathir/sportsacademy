from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import UserRole
from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return await self.db.scalar(stmt)

    async def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return await self.db.scalar(stmt)

    async def admin_exists(self) -> bool:
        stmt = select(User.id).where(User.role == UserRole.admin).limit(1)
        return await self.db.scalar(stmt) is not None

    async def list_students(self) -> list[User]:
        stmt = select(User).where(User.role == UserRole.student).order_by(User.created_at.desc())
        result = await self.db.scalars(stmt)
        return list(result.all())

    def add(self, user: User) -> User:
        self.db.add(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
