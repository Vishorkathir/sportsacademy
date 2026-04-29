# Cricket Academy Admission and Fee API

FastAPI backend for managing:

- admin and student authentication
- student onboarding and admission
- fee plans
- offline payment notifications
- approved and manual payment records

## Overview

This API is role-based and centers on a simple academy workflow:

1. Bootstrap the first admin
2. Admin logs in
3. Admin creates a student account and fee plan
4. Admin admits the student
5. Student logs in
6. Student submits an offline payment notification
7. Admin approves or rejects that notification
8. Approved notifications become official payments

Authentication is JWT-based. The API supports both:

- `Authorization: Bearer <token>`
- an HTTP-only cookie set by the login endpoints

## Tech stack

- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL
- Alembic
- Pydantic Settings
- `python-jose` for JWTs
- pytest, pytest-asyncio, and httpx for tests

## Project structure

```text
.
├── alembic/
├── app/
│   ├── auth/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   └── services/
├── tests/
├── .env.example
├── main.py
├── pyproject.toml
└── README.md
```

## Domain model

Primary tables:

- `users`
- `student_profiles`
- `admissions`
- `fee_plans`
- `payment_notifications`
- `payments`

Important enum values used by the API:

- Roles: `admin`, `student`
- Admission statuses: `pending`, `admitted`, `rejected`
- Notification statuses: `pending`, `approved`, `rejected`
- Payment sources: `manual`, `notification`
- Derived payment statuses: `nopaid`, `halfpayed`, `fulpayed`
- Student skills: `Batting`, `Bowling`, `Wicket Keeping`

## Environment variables

Settings are loaded from `backend/.env`.

Create that file from `.env.example`:

```bash
cp .env.example .env
```

Example values:

```env
DATABASE_URL=postgresql+asyncpg://postgres:your-password@localhost:5432/cricket_academy
AUTO_CREATE_TABLES_ON_STARTUP=true
JWT_SECRET_KEY=replace-with-a-strong-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AUTH_COOKIE_NAME=access_token
AUTH_COOKIE_SECURE=false
AUTH_COOKIE_SAMESITE=lax
```

Notes:

- `DATABASE_URL` is required
- `JWT_SECRET_KEY` is required
- `AUTO_CREATE_TABLES_ON_STARTUP=true` makes the app attempt schema creation at startup
- Alembic migrations are still the preferred way to manage schema changes

## Local setup

Requires Python `>=3.10`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn main:app --reload
```

Useful URLs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

## API behavior

### Auth rules

- The first admin can register without authentication
- After an admin exists, only an authenticated admin can create more admins
- Admin and student login routes are separate
- Login endpoints accept JSON bodies, not form-encoded payloads
- Admin tokens cannot access student-only routes
- Student tokens cannot access admin-only routes

### Payment rules

- Students never create final payment records directly
- Students submit `payment_notifications`
- Admins approve or reject notifications
- Approval creates the real `payments` row
- Admins may also create manual payments directly

## Main flow

### 1. Bootstrap the first admin

`POST /auth/admin/register`

```json
{
  "email": "admin@example.com",
  "full_name": "System Admin",
  "password": "admin123"
}
```

### 2. Admin login

`POST /auth/admin/login`

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

Example response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### 3. Create a student

`POST /admin/students`

```json
{
  "email": "student1@example.com",
  "full_name": "Student One",
  "password": "secret123",
  "phone": "9999999999",
  "address": "Pune",
  "guardian_name": "Parent One",
  "guardian_phone": "8888888888",
  "skills": ["Batting", "Bowling"],
  "total_fee": 120000,
  "currency": "INR"
}
```

This creates:

- the student user
- student profile
- pending admission record
- fee plan

### 4. Admit the student

`POST /admin/admit/{student_id}`

```json
{
  "remarks": "Qualified for admission"
}
```

### 5. Student login

`POST /auth/student/login`

```json
{
  "email": "student1@example.com",
  "password": "secret123"
}
```

### 6. Student submits a payment notification

`POST /student/payment-notification`

```json
{
  "claimed_amount": 60000,
  "payment_date": "2026-04-26",
  "payment_mode": "bank_transfer",
  "reference_no": "UTR123456",
  "note": "Paid at bank branch"
}
```

### 7. Admin approves a payment notification

`POST /admin/payment-notifications/{id}/approve`

```json
{
  "approved_amount": 60000,
  "paid_on": "2026-04-26",
  "admin_remark": "Verified with bank statement"
}
```

### 8. Admin can also record a manual payment

`POST /admin/payments/manual`

```json
{
  "student_id": "00000000-0000-0000-0000-000000000001",
  "amount": 10000,
  "paid_on": "2026-04-26",
  "mode": "cash",
  "reference_no": null,
  "note": "Collected at office"
}
```

## Endpoint reference

### Health

- `GET /health`

### Auth

- `POST /auth/admin/register`
- `POST /auth/admin/login`
- `POST /auth/admin/logout`
- `POST /auth/student/login`
- `POST /auth/student/logout`

### Admin

- `POST /admin/students`
- `PATCH /admin/students/{student_id}`
- `GET /admin/students`
- `DELETE /admin/students/{student_id}`
- `POST /admin/admit/{student_id}`
- `GET /admin/payment-notifications`
- `POST /admin/payment-notifications/{id}/approve`
- `POST /admin/payment-notifications/{id}/reject`
- `POST /admin/payments/manual`
- `GET /admin/students/{student_id}/payments`

### Student

- `GET /student/me`
- `GET /student/admission`
- `GET /student/payments`
- `POST /student/payment-notification`

## Tests

The test suite uses an in-memory SQLite database with `aiosqlite` and covers:

- health check
- admin bootstrap and login rules
- student/admin role restrictions
- student CRUD
- admission flow
- notification approval flow
- manual payments
- student payment summaries

Run tests with:

```bash
python -m pytest tests -v
```

## Production notes

- Replace the sample `JWT_SECRET_KEY` with a strong random secret
- Set `AUTH_COOKIE_SECURE=true` behind HTTPS
- Review `AUTH_COOKIE_SAMESITE` for your deployment needs
- Restrict who can reach admin registration after bootstrap
- Prefer migrations over startup table creation for controlled deployments
