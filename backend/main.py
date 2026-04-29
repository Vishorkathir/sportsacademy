from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.student import router as student_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        if settings.auto_create_tables_on_startup:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
    except Exception:
        # Database may not be initialized yet; app can still start for migration workflows
        pass
    yield


API_DESCRIPTION = """
JWT-protected API for cricket academy admission and offline fee tracking.

Workflow:
1. Bootstrap the first admin with `/auth/admin/register`.
2. Admin logs in and creates student accounts.
3. Admin admits a student with `/admin/admit/{student_id}`.
4. Student logs in and submits offline payment notifications.
5. Admin approves or rejects notifications, or records manual payments directly.
6. Student and admin both view payment history from their role-specific endpoints.
""".strip()


app = FastAPI(title=settings.project_name, description=API_DESCRIPTION, version="1.0.0", lifespan=lifespan)


# Test app without lifespan (for pytest)
test_app = FastAPI(title=settings.project_name, description=API_DESCRIPTION, version="1.0.0")

for _app in [app, test_app]:
    _app.include_router(auth_router)
    _app.include_router(admin_router)
    _app.include_router(student_router)


@app.get("/health")
@test_app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
