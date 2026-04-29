from collections.abc import Callable
from uuid import UUID

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import decode_access_token
from app.core.config import settings
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def _resolve_user_from_token(token: str, db: AsyncSession) -> User:
    try:
        payload = decode_access_token(token)
        user_id_raw = payload.get("sub")
        if not user_id_raw:
            raise ValueError("Missing subject")
        user_id = UUID(user_id_raw)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc

    user = await UserRepository(db).get_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user


async def get_current_user(
    bearer_credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    cookie_token: str | None = Cookie(default=None, alias=settings.auth_cookie_name),
    db: AsyncSession = Depends(get_db),
) -> User:
    bearer_token = bearer_credentials.credentials if bearer_credentials else None
    token = cookie_token or bearer_token
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return await _resolve_user_from_token(token, db)


async def get_current_user_optional(
    bearer_credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    cookie_token: str | None = Cookie(default=None, alias=settings.auth_cookie_name),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    bearer_token = bearer_credentials.credentials if bearer_credentials else None
    token = cookie_token or bearer_token
    if not token:
        return None
    return await _resolve_user_from_token(token, db)


def require_role(role: UserRole) -> Callable:
    async def _require(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user

    return _require


async def get_current_admin(user: User = Depends(require_role(UserRole.admin))) -> User:
    return user


async def get_current_student(user: User = Depends(require_role(UserRole.student))) -> User:
    return user
