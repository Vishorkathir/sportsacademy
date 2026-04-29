from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import create_access_token, get_password_hash, verify_password
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AdminRegisterRequest, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_repo = UserRepository(db)

    async def admin_exists(self) -> bool:
        return await self.user_repo.admin_exists()

    async def register_admin(self, payload: AdminRegisterRequest) -> User:
        existing = await self.user_repo.get_by_email(payload.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")

        admin = User(
            email=payload.email,
            full_name=payload.full_name,
            hashed_password=get_password_hash(payload.password),
            role=UserRole.admin,
            is_active=True,
        )
        self.user_repo.add(admin)
        await self.db.commit()
        await self.db.refresh(admin)
        return admin

    async def login(self, email: str, password: str, required_role: UserRole | None = None) -> TokenResponse:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        if required_role and user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This login endpoint is only for {required_role.value} users",
            )

        token = create_access_token(str(user.id))
        return TokenResponse(access_token=token)
