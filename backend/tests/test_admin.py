"""Tests for admin endpoints."""

from httpx import AsyncClient


class TestAdminCreateStudent:
    """Test student creation by admin."""

    async def test_create_student_success(self, client: AsyncClient, admin_auth_headers: dict):
        """Test successful student creation."""
        payload = {
            "email": "newstudent@test.local",
            "full_name": "New Student",
            "password": "secure123",
            "phone": "9876543210",
            "address": "New Address",
            "guardian_name": "Guardian",
            "guardian_phone": "9123456789",
            "skills": ["Batting", "Wicket Keeping"],
            "total_fee": 150000,
            "currency": "INR",
        }

        response = await client.post("/admin/students", json=payload, headers=admin_auth_headers)

        assert response.status_code == 201
        data = response.json()

        assert data["user"]["email"] == "newstudent@test.local"
        assert data["user"]["full_name"] == "New Student"
        assert data["user"]["role"] == "student"

        assert data["profile"]["phone"] == "9876543210"
        assert data["profile"]["address"] == "New Address"
        assert data["profile"]["skills"] == ["Batting", "Wicket Keeping"]

        assert data["admission"]["status"] == "pending"

        assert data["fee_plan"]["total_fee"] == 150000
        assert data["fee_plan"]["currency"] == "INR"

    async def test_create_student_duplicate_email(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test student creation with duplicate email."""
        payload = {
            "email": student_user.email,
            "full_name": "Another Student",
            "password": "password123",
            "total_fee": 100000,
        }

        response = await client.post("/admin/students", json=payload, headers=admin_auth_headers)

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_create_student_rejects_invalid_skill(self, client: AsyncClient, admin_auth_headers: dict):
        """Test student creation validates allowed skill values."""
        payload = {
            "email": "newstudent@test.local",
            "full_name": "New Student",
            "password": "password123",
            "skills": ["Fielding"],
            "total_fee": 100000,
        }

        response = await client.post("/admin/students", json=payload, headers=admin_auth_headers)

        assert response.status_code == 422

    async def test_create_student_unauthorized(self, client: AsyncClient):
        """Test student creation without authentication."""
        payload = {
            "email": "newstudent@test.local",
            "full_name": "New Student",
            "password": "password123",
            "total_fee": 100000,
        }

        response = await client.post("/admin/students", json=payload)

        assert response.status_code == 403

    async def test_create_student_rejects_student_token(self, client: AsyncClient, student_auth_headers: dict):
        """Test student token cannot create student accounts."""
        payload = {
            "email": "newstudent@test.local",
            "full_name": "New Student",
            "password": "password123",
            "total_fee": 100000,
        }

        response = await client.post("/admin/students", json=payload, headers=student_auth_headers)

        assert response.status_code == 403


class TestAdminAdmitStudent:
    """Test student admission by admin."""

    async def test_admit_student_success(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test successful student admission."""
        response = await client.post(
            f"/admin/admit/{student_user.id}",
            json={"remarks": "Qualified for admission"},
            headers=admin_auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "admitted"
        assert data["remarks"] == "Qualified for admission"
        assert data["admitted_at"] is not None

    async def test_admit_student_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test admission of non-existent student."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.post(
            f"/admin/admit/{fake_id}",
            json={"remarks": "Test"},
            headers=admin_auth_headers,
        )

        assert response.status_code == 404


class TestAdminUpdateStudent:
    """Test student updates by admin."""

    async def test_update_student_success(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test successful student update."""
        response = await client.patch(
            f"/admin/students/{student_user.id}",
            json={
                "email": "updatedstudent@test.local",
                "full_name": "Updated Student",
                "phone": "7777777777",
                "address": "Updated Address",
                "guardian_name": "Updated Guardian",
                "guardian_phone": "6666666666",
                "skills": ["Bowling", "Wicket Keeping"],
                "total_fee": 125000,
                "currency": "USD",
            },
            headers=admin_auth_headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == "updatedstudent@test.local"
        assert data["user"]["full_name"] == "Updated Student"
        assert data["profile"]["phone"] == "7777777777"
        assert data["profile"]["skills"] == ["Bowling", "Wicket Keeping"]
        assert data["fee_plan"]["total_fee"] == 125000
        assert data["fee_plan"]["currency"] == "USD"

    async def test_update_student_duplicate_email(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test student update with existing email."""
        await client.post(
            "/admin/students",
            json={
                "email": "otherstudent@test.local",
                "full_name": "Other Student",
                "password": "password123",
                "total_fee": 100000,
            },
            headers=admin_auth_headers,
        )

        response = await client.patch(
            f"/admin/students/{student_user.id}",
            json={"email": "otherstudent@test.local"},
            headers=admin_auth_headers,
        )

        assert response.status_code == 409

    async def test_update_student_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test updating a non-existent student."""
        response = await client.patch(
            "/admin/students/00000000-0000-0000-0000-000000000000",
            json={"full_name": "Missing Student"},
            headers=admin_auth_headers,
        )

        assert response.status_code == 404


class TestAdminDeleteStudent:
    """Test student deletion by admin."""

    async def test_delete_student_success(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test successful student deletion."""
        response = await client.delete(f"/admin/students/{student_user.id}", headers=admin_auth_headers)

        assert response.status_code == 204

        list_response = await client.get("/admin/students", headers=admin_auth_headers)
        assert list_response.status_code == 200
        data = list_response.json()
        assert all(student["id"] != str(student_user.id) for student in data)

    async def test_delete_student_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test deleting a non-existent student."""
        response = await client.delete(
            "/admin/students/00000000-0000-0000-0000-000000000000",
            headers=admin_auth_headers,
        )

        assert response.status_code == 404


class TestAdminListStudents:
    """Test listing students."""

    async def test_list_students_success(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test listing all students."""
        response = await client.get("/admin/students", headers=admin_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(s["email"] == student_user.email for s in data)

    async def test_list_students_unauthorized(self, client: AsyncClient):
        """Test listing students without authentication."""
        response = await client.get("/admin/students")

        assert response.status_code == 403


class TestAdminPaymentNotifications:
    """Test payment notification management."""

    async def test_list_payment_notifications_empty(self, client: AsyncClient, admin_auth_headers: dict):
        """Test listing payment notifications when none exist."""
        response = await client.get("/admin/payment-notifications", headers=admin_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_approve_notification_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test approving non-existent notification."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.post(
            f"/admin/payment-notifications/{fake_id}/approve",
            json={"approved_amount": 50000},
            headers=admin_auth_headers,
        )

        assert response.status_code == 404

    async def test_reject_notification_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test rejecting non-existent notification."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = await client.post(
            f"/admin/payment-notifications/{fake_id}/reject",
            json={"admin_remark": "Not verified"},
            headers=admin_auth_headers,
        )

        assert response.status_code == 404


class TestAdminManualPayment:
    """Test manual payment creation by admin."""

    async def test_add_manual_payment_success(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test successful manual payment creation."""
        payload = {
            "student_id": str(student_user.id),
            "amount": 50000,
            "paid_on": "2026-04-20",
            "mode": "bank_transfer",
            "reference_no": "TXN123456",
            "note": "Payment verified",
        }

        response = await client.post("/admin/payments/manual", json=payload, headers=admin_auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["amount"] == 50000
        assert data["source"] == "manual"
        assert data["mode"] == "bank_transfer"

    async def test_add_manual_payment_student_not_found(self, client: AsyncClient, admin_auth_headers: dict):
        """Test manual payment for non-existent student."""
        payload = {
            "student_id": "00000000-0000-0000-0000-000000000000",
            "amount": 50000,
            "paid_on": "2026-04-20",
            "mode": "bank_transfer",
        }

        response = await client.post("/admin/payments/manual", json=payload, headers=admin_auth_headers)

        assert response.status_code == 404


class TestAdminPaymentHistory:
    """Test student payment history retrieval."""

    async def test_get_payment_history_no_payments(self, client: AsyncClient, admin_auth_headers: dict, student_user):
        """Test payment history for student with no payments."""
        response = await client.get(f"/admin/students/{student_user.id}/payments", headers=admin_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["payment_status"] == "nopaid"
        assert data["total_approved_amount"] == 0
        assert len(data["payments"]) == 0

    async def test_get_payment_history_with_payment(
        self, client: AsyncClient, admin_auth_headers: dict, student_user
    ):
        """Test payment history after adding manual payment."""
        # Add a manual payment first
        await client.post(
            "/admin/payments/manual",
            json={
                "student_id": str(student_user.id),
                "amount": 50000,
                "paid_on": "2026-04-20",
                "mode": "bank_transfer",
            },
            headers=admin_auth_headers,
        )

        response = await client.get(f"/admin/students/{student_user.id}/payments", headers=admin_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["payment_status"] == "halfpayed"
        assert data["total_approved_amount"] == 50000
        assert len(data["payments"]) == 1
