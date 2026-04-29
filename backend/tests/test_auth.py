"""Tests for authentication endpoints."""

from httpx import AsyncClient


class TestAdminRegistration:
    """Test admin registration flow."""

    async def test_first_admin_can_register_without_token(self, client: AsyncClient):
        """Test bootstrap registration when no admin exists."""
        response = await client.post(
            "/auth/admin/register",
            json={
                "email": "first-admin@test.local",
                "full_name": "First Admin",
                "password": "admin123",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == "first-admin@test.local"
        assert data["user"]["role"] == "admin"

    async def test_register_admin_requires_admin_token_when_admin_exists(self, client: AsyncClient, admin_user):
        """Test registration is protected once an admin exists."""
        response = await client.post(
            "/auth/admin/register",
            json={
                "email": "second-admin@test.local",
                "full_name": "Second Admin",
                "password": "admin123",
            },
        )

        assert response.status_code == 401
        assert "Admin authentication required" in response.json()["detail"]

    async def test_student_cannot_register_admin(self, client: AsyncClient, student_auth_headers: dict, admin_user):
        """Test student token cannot create admins."""
        response = await client.post(
            "/auth/admin/register",
            json={
                "email": "second-admin@test.local",
                "full_name": "Second Admin",
                "password": "admin123",
            },
            headers=student_auth_headers,
        )

        assert response.status_code == 403
        assert "Only admins can register new admins" in response.json()["detail"]

    async def test_admin_can_register_another_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test existing admin can create another admin."""
        response = await client.post(
            "/auth/admin/register",
            json={
                "email": "second-admin@test.local",
                "full_name": "Second Admin",
                "password": "admin123",
            },
            headers=admin_auth_headers,
        )

        assert response.status_code == 201
        data = response.json()
        assert data["user"]["email"] == "second-admin@test.local"
        assert data["user"]["role"] == "admin"

    async def test_register_admin_duplicate_email(self, client: AsyncClient, admin_auth_headers: dict, admin_user):
        """Test admin registration rejects duplicate email."""
        response = await client.post(
            "/auth/admin/register",
            json={
                "email": admin_user.email,
                "full_name": "Duplicate Admin",
                "password": "admin123",
            },
            headers=admin_auth_headers,
        )

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


class TestAdminLogin:
    """Test admin login endpoint."""

    async def test_admin_login_success(self, client: AsyncClient, admin_user):
        """Test admin-specific login endpoint."""
        response = await client.post(
            "/auth/admin/login",
            json={"email": admin_user.email, "password": "admin123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert response.request.headers["content-type"].startswith("application/json")

    async def test_admin_login_rejects_student(self, client: AsyncClient, student_user):
        """Test admin login endpoint rejects student credentials."""
        response = await client.post(
            "/auth/admin/login",
            json={"email": student_user.email, "password": "student123"},
        )

        assert response.status_code == 403

    async def test_admin_login_rejects_form_encoded_payload(self, client: AsyncClient, admin_user):
        """Test admin login no longer accepts form-encoded payloads."""
        response = await client.post(
            "/auth/admin/login",
            data={"username": admin_user.email, "password": "admin123"},
        )

        assert response.status_code == 422


class TestAdminLogout:
    """Test admin logout endpoint."""

    async def test_admin_logout_success(self, client: AsyncClient, admin_auth_headers: dict):
        """Test admin logout clears cookie."""
        response = await client.post("/auth/admin/logout", headers=admin_auth_headers)

        assert response.status_code == 204
        set_cookie = response.headers.get("set-cookie", "")
        assert "access_token=" in set_cookie

    async def test_admin_logout_rejects_student(self, client: AsyncClient, student_auth_headers: dict):
        """Test student token cannot use admin logout."""
        response = await client.post("/auth/admin/logout", headers=student_auth_headers)

        assert response.status_code == 403


class TestStudentLogin:
    """Test student login endpoint."""

    async def test_student_login_success(self, client: AsyncClient, student_user):
        """Test student-specific login endpoint."""
        response = await client.post(
            "/auth/student/login",
            json={"email": student_user.email, "password": "student123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_student_login_rejects_admin(self, client: AsyncClient, admin_user):
        """Test student login endpoint rejects admin credentials."""
        response = await client.post(
            "/auth/student/login",
            json={"email": admin_user.email, "password": "admin123"},
        )

        assert response.status_code == 403

    async def test_student_login_rejects_form_encoded_payload(self, client: AsyncClient, student_user):
        """Test student login no longer accepts form-encoded payloads."""
        response = await client.post(
            "/auth/student/login",
            data={"username": student_user.email, "password": "student123"},
        )

        assert response.status_code == 422

    async def test_removed_generic_login_route(self, client: AsyncClient):
        """Test generic login route is no longer available."""
        response = await client.post(
            "/auth/login",
            json={"email": "anyone@test.local", "password": "admin123"},
        )

        assert response.status_code == 404


class TestStudentLogout:
    """Test student logout endpoint."""

    async def test_student_logout_success(self, client: AsyncClient, student_auth_headers: dict):
        """Test student logout clears cookie."""
        response = await client.post("/auth/student/logout", headers=student_auth_headers)

        assert response.status_code == 204
        set_cookie = response.headers.get("set-cookie", "")
        assert "access_token=" in set_cookie

    async def test_student_logout_rejects_admin(self, client: AsyncClient, admin_auth_headers: dict):
        """Test admin token cannot use student logout."""
        response = await client.post("/auth/student/logout", headers=admin_auth_headers)

        assert response.status_code == 403
