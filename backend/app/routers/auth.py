from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_admin, get_current_student, get_current_user_optional
from app.core.config import settings
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import AdminRegisterRequest, AdminRegisterResponse, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


def _set_auth_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key=settings.auth_cookie_name,
        value=access_token,
        httponly=True,
        secure=settings.auth_cookie_secure,
        samesite=settings.auth_cookie_samesite,
        max_age=settings.access_token_expire_minutes * 60,
    )


def _clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key=settings.auth_cookie_name)


@router.post(
    "/admin/register",
    response_model=AdminRegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register an admin account",
    description=(
        "Bootstrap the first admin when no admin exists. After bootstrap, only an authenticated admin "
        "can create additional admin accounts."
    ),
)
async def admin_register(
    payload: AdminRegisterRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    service = AuthService(db)
    if await service.admin_exists():
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin authentication required")
        if current_user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admins can register new admins",
            )

    admin = await service.register_admin(payload)
    return AdminRegisterResponse(user=admin)


@router.post(
    "/admin/login",
    response_model=TokenResponse,
    summary="Login as admin",
    description="Authenticate an admin from a JSON email/password payload and return a JWT access token.",
)
async def admin_login(
    response: Response,
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    token_response = await service.login(payload.email, payload.password, required_role=UserRole.admin)
    _set_auth_cookie(response, token_response.access_token)
    return token_response


@router.post(
    "/admin/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout admin",
    description="Clear the auth cookie for the currently authenticated admin session.",
)
async def admin_logout(response: Response, _: User = Depends(get_current_admin)) -> None:
    _clear_auth_cookie(response)


@router.post(
    "/student/login",
    response_model=TokenResponse,
    summary="Login as student",
    description="Authenticate a student from a JSON email/password payload and return a JWT access token.",
)
async def student_login(
    response: Response,
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    token_response = await service.login(payload.email, payload.password, required_role=UserRole.student)
    _set_auth_cookie(response, token_response.access_token)
    return token_response


@router.post(
    "/student/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Logout student",
    description="Clear the auth cookie for the currently authenticated student session.",
)
async def student_logout(response: Response, _: User = Depends(get_current_student)) -> None:
    _clear_auth_cookie(response)
