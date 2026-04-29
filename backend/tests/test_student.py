"""Tests for student endpoints."""

from httpx import AsyncClient


class TestStudentProfile:
    """Test student profile endpoints."""

    async def test_get_student_profile_success(self, client: AsyncClient, student_auth_headers: dict, student_user):
        """Test retrieving own profile."""
        response = await client.get("/student/me", headers=student_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["user"]["email"] == student_user.email
        assert data["user"]["full_name"] == student_user.full_name
        assert data["profile"]["phone"] == "9999999999"
        assert data["profile"]["skills"] == ["Batting", "Bowling"]

    async def test_get_student_profile_unauthorized(self, client: AsyncClient):
        """Test profile endpoint without authentication."""
        response = await client.get("/student/me")

        assert response.status_code == 403

    async def test_get_student_profile_rejects_admin_token(self, client: AsyncClient, admin_auth_headers: dict):
        """Test admin token cannot access student profile endpoint."""
        response = await client.get("/student/me", headers=admin_auth_headers)

        assert response.status_code == 403


class TestStudentAdmission:
    """Test student admission status endpoints."""

    async def test_get_admission_pending(self, client: AsyncClient, student_auth_headers: dict):
        """Test admission status when pending."""
        response = await client.get("/student/admission", headers=student_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["admission"]["status"] == "pending"
        assert data["total_approved_amount"] == 0
        assert data["payment_status"] == "nopaid"

    async def test_get_admission_admitted(self, client: AsyncClient, admitted_student_auth_headers: dict):
        """Test admission status when admitted."""
        response = await client.get("/student/admission", headers=admitted_student_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["admission"]["status"] == "admitted"
        assert data["admission"]["admitted_at"] is not None


class TestStudentPayments:
    """Test student payment endpoints."""

    async def test_get_payments_empty(self, client: AsyncClient, student_auth_headers: dict):
        """Test payment list when no payments exist."""
        response = await client.get("/student/payments", headers=student_auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["payment_status"] == "nopaid"
        assert data["total_approved_amount"] == 0
        assert len(data["payments"]) == 0
        assert data["fee_plan"]["total_fee"] == 100000

    async def test_get_payments_unauthorized(self, client: AsyncClient):
        """Test payment endpoint without authentication."""
        response = await client.get("/student/payments")

        assert response.status_code == 403


class TestStudentPaymentNotification:
    """Test student payment notification submission."""

    async def test_submit_notification_pending_admission(
        self, client: AsyncClient, student_auth_headers: dict
    ):
        """Test payment notification submission when student is not admitted."""
        payload = {
            "claimed_amount": 50000,
            "payment_date": "2026-04-20",
            "payment_mode": "bank_transfer",
            "reference_no": "UTR123456",
            "note": "Paid at bank",
        }

        response = await client.post(
            "/student/payment-notification", json=payload, headers=student_auth_headers
        )

        assert response.status_code == 400
        assert "not admitted yet" in response.json()["detail"]

    async def test_submit_notification_success(
        self, client: AsyncClient, admitted_student_auth_headers: dict
    ):
        """Test successful payment notification submission."""
        payload = {
            "claimed_amount": 50000,
            "payment_date": "2026-04-20",
            "payment_mode": "bank_transfer",
            "reference_no": "UTR123456",
            "note": "Paid at bank",
        }

        response = await client.post(
            "/student/payment-notification", json=payload, headers=admitted_student_auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["claimed_amount"] == 50000
        assert data["payment_mode"] == "bank_transfer"
        assert data["status"] == "pending"
        assert data["reference_no"] == "UTR123456"

    async def test_submit_notification_unauthorized(self, client: AsyncClient):
        """Test notification submission without authentication."""
        payload = {
            "claimed_amount": 50000,
            "payment_date": "2026-04-20",
            "payment_mode": "bank_transfer",
        }

        response = await client.post("/student/payment-notification", json=payload)

        assert response.status_code == 403


class TestStudentPaymentWorkflow:
    """Test complete payment workflow."""

    async def test_notification_to_payment_flow(
        self, client: AsyncClient, admin_auth_headers: dict, admitted_student_auth_headers: dict
    ):
        """Test end-to-end: notification submission -> admin approval."""
        # Step 1: Student submits notification
        notification_payload = {
            "claimed_amount": 50000,
            "payment_date": "2026-04-20",
            "payment_mode": "bank_transfer",
            "reference_no": "UTR123456",
        }

        notification_response = await client.post(
            "/student/payment-notification",
            json=notification_payload,
            headers=admitted_student_auth_headers,
        )

        assert notification_response.status_code == 201
        notification_id = notification_response.json()["id"]

        # Step 2: Admin lists notifications
        list_response = await client.get("/admin/payment-notifications", headers=admin_auth_headers)
        assert list_response.status_code == 200
        data = list_response.json()
        assert len(data) == 1
        assert data[0]["status"] == "pending"

        # Step 3: Admin approves notification
        approve_payload = {"approved_amount": 50000, "paid_on": "2026-04-20"}

        approve_response = await client.post(
            f"/admin/payment-notifications/{notification_id}/approve",
            json=approve_payload,
            headers=admin_auth_headers,
        )

        assert approve_response.status_code == 200
        assert approve_response.json()["amount"] == 50000
        assert approve_response.json()["source"] == "notification"

        # Step 4: Student checks updated payment status
        payments_response = await client.get("/student/payments", headers=admitted_student_auth_headers)

        assert payments_response.status_code == 200
        data = payments_response.json()
        assert data["payment_status"] == "halfpayed"
        assert data["total_approved_amount"] == 50000
        assert len(data["payments"]) == 1
