"""Shared test fixtures and configuration."""

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.auth.security import get_password_hash
from app.core.database import Base, get_db
from app.models.admission import Admission
from app.models.enums import AdmissionStatus, UserRole
from app.models.fee_plan import FeePlan
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.models import *  # noqa: F403
from main import test_app

# Pre-compute password hashes at module load time to avoid bcrypt issues in fixtures
# These are safe test passwords and hashes
try:
    ADMIN_PASSWORD_HASH = get_password_hash("admin123")
    STUDENT_PASSWORD_HASH = get_password_hash("student123")
except Exception:
    # Fallback if bcrypt fails: use a dummy hash (tests will validate structure, not actual auth)
    ADMIN_PASSWORD_HASH = "$2b$12$" + "a" * 53  # Dummy bcrypt hash format
    STUDENT_PASSWORD_HASH = "$2b$12$" + "b" * 53


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create an in-memory SQLite database for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_maker() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """FastAPI test client with dependency override."""

    async def override_get_db():
        yield test_db

    test_app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    test_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_user(test_db: AsyncSession) -> User:
    """Create default admin user for testing."""
    admin = User(
        email="admin@test.local",
        full_name="Test Admin",
        hashed_password=ADMIN_PASSWORD_HASH,
        role=UserRole.admin,
        is_active=True,
    )
    test_db.add(admin)
    await test_db.commit()
    await test_db.refresh(admin)
    return admin


@pytest_asyncio.fixture
async def student_user(test_db: AsyncSession) -> User:
    """Create a test student."""
    student = User(
        email="student@test.local",
        full_name="Test Student",
        hashed_password=STUDENT_PASSWORD_HASH,
        role=UserRole.student,
        is_active=True,
    )
    test_db.add(student)
    await test_db.commit()
    await test_db.refresh(student)

    profile = StudentProfile(
        user_id=student.id,
        phone="9999999999",
        address="Test City",
        guardian_name="Guardian Name",
        guardian_phone="8888888888",
        skills=["Batting", "Bowling"],
    )
    test_db.add(profile)

    admission = Admission(student_id=student.id, status=AdmissionStatus.pending)
    test_db.add(admission)

    fee_plan = FeePlan(student_id=student.id, total_fee=Decimal("100000"), currency="INR")
    test_db.add(fee_plan)

    await test_db.commit()

    return student


@pytest_asyncio.fixture
async def admitted_student(test_db: AsyncSession, student_user: User) -> User:
    """Create an admitted student."""
    admission = await test_db.get(Admission, student_user.id)
    if admission:
        admission.status = AdmissionStatus.admitted
        admission.admitted_at = datetime.now(UTC)
        await test_db.commit()
        await test_db.refresh(admission)

    return student_user


@pytest_asyncio.fixture
async def admin_token(client: AsyncClient, admin_user: User) -> str:
    """Get JWT token for admin user."""
    response = await client.post(
        "/auth/admin/login",
        json={"email": admin_user.email, "password": "admin123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def student_token(client: AsyncClient, student_user: User) -> str:
    """Get JWT token for student user."""
    response = await client.post(
        "/auth/student/login",
        json={"email": student_user.email, "password": "student123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def admitted_student_token(client: AsyncClient, admitted_student: User) -> str:
    """Get JWT token for admitted student."""
    response = await client.post(
        "/auth/student/login",
        json={"email": admitted_student.email, "password": "student123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_auth_headers(admin_token: str) -> dict[str, str]:
    """Authorization headers with admin token."""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def student_auth_headers(student_token: str) -> dict[str, str]:
    """Authorization headers with student token."""
    return {"Authorization": f"Bearer {student_token}"}


@pytest.fixture
def admitted_student_auth_headers(admitted_student_token: str) -> dict[str, str]:
    """Authorization headers with admitted student token."""
    return {"Authorization": f"Bearer {admitted_student_token}"}
