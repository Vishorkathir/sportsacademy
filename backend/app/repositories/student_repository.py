from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admission import Admission
from app.models.fee_plan import FeePlan
from app.models.student_profile import StudentProfile


class StudentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_profile(self, student_id: UUID) -> StudentProfile | None:
        return await self.db.scalar(select(StudentProfile).where(StudentProfile.user_id == student_id))

    async def get_admission(self, student_id: UUID) -> Admission | None:
        return await self.db.scalar(select(Admission).where(Admission.student_id == student_id))

    async def get_fee_plan(self, student_id: UUID) -> FeePlan | None:
        return await self.db.scalar(select(FeePlan).where(FeePlan.student_id == student_id))

    def add_profile(self, profile: StudentProfile) -> StudentProfile:
        self.db.add(profile)
        return profile

    def add_admission(self, admission: Admission) -> Admission:
        self.db.add(admission)
        return admission

    def add_or_update_fee_plan(self, fee_plan: FeePlan) -> FeePlan:
        self.db.add(fee_plan)
        return fee_plan

    async def delete_profile(self, profile: StudentProfile) -> None:
        await self.db.delete(profile)

    async def delete_admission(self, admission: Admission) -> None:
        await self.db.delete(admission)

    async def delete_fee_plan(self, fee_plan: FeePlan) -> None:
        await self.db.delete(fee_plan)
