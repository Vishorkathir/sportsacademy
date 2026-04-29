# Sports Academy

Sports Academy is a two-part project with:

- a FastAPI backend for academy admission, authentication, and offline fee tracking
- a React + Vite frontend for the academy admin portal UI

The backend is the functional core of the project today. The frontend already has a polished admin-facing interface, but only the login screen is wired to the API right now. The dashboard and registration views still use static/demo data.

## What the backend does

The API supports a role-based academy workflow:

1. Bootstrap the first admin with `POST /auth/admin/register`
2. Admin logs in with `POST /auth/admin/login`
3. Admin creates student accounts and fee plans
4. Admin admits a student
5. Student logs in with `POST /auth/student/login`
6. Student submits an offline payment notification
7. Admin approves or rejects the notification
8. Approved notifications become official payment records
9. Admin or student can view payment history from role-specific endpoints

### Core backend features

- JWT-based authentication for admins and students
- HTTP-only auth cookie support alongside `Authorization: Bearer <token>`
- first-admin bootstrap flow
- student creation, update, listing, and deletion
- admission state tracking
- fee-plan tracking
- offline payment notification workflow
- admin manual payment entry
- derived payment status values:
  `nopaid`, `halfpayed`, `fulpayed`

### Domain values used in code

- Roles: `admin`, `student`
- Admission statuses: `pending`, `admitted`, `rejected`
- Notification statuses: `pending`, `approved`, `rejected`
- Payment sources: `manual`, `notification`
- Student skills: `Batting`, `Bowling`, `Wicket Keeping`

## What the frontend does

The frontend is a React 19 + Vite application styled with MUI and Tailwind tooling.

### Current screens

- `/` and `/login`
  Admin login page
- `/dashboard`
  Admin dashboard overview
- `/registration`
  Student registration/profile screen

### Current integration status

- The login page sends a request to `POST /auth/admin/login`
- It reads the API base URL from `VITE_API_BASE_URL`
- On success it stores the returned token in `localStorage` under `kings11_admin_token`
- The dashboard, broadcast panel, and registration page currently render mock/static data

## Tech stack

### Backend

- FastAPI
- SQLAlchemy 2.0 async
- PostgreSQL
- Alembic
- Pydantic Settings
- JWT via `python-jose`
- pytest + pytest-asyncio + httpx for tests

### Frontend

- React 19
- Vite
- React Router
- MUI
- Tailwind/PostCSS tooling

## Repository structure

```text
.
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── .env.example
│   ├── main.py
│   └── pyproject.toml
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API routes

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

## Request shapes worth knowing

### Admin login

```json
{
  "email": "admin@example.com",
  "password": "admin123"
}
```

### Student creation

```json
{
  "email": "student@example.com",
  "full_name": "New Student",
  "password": "secure123",
  "phone": "9876543210",
  "address": "Bengaluru",
  "guardian_name": "Parent Name",
  "guardian_phone": "9123456789",
  "skills": ["Batting", "Wicket Keeping"],
  "total_fee": 150000,
  "currency": "INR"
}
```

### Student payment notification

```json
{
  "claimed_amount": 50000,
  "payment_date": "2026-04-20",
  "payment_mode": "bank_transfer",
  "reference_no": "UTR123456",
  "note": "Paid at bank"
}
```

## Environment variables

### Backend

The backend reads its settings from `backend/.env`.

Create `backend/.env` from `backend/.env.example`.

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

### Frontend

Optional:

```env
VITE_API_BASE_URL=http://localhost:8000
```

If unset, the frontend defaults to `http://localhost:8000`.

## Local development

### 1. Start the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn main:app --reload
```

Backend URLs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

Note:
If `AUTO_CREATE_TABLES_ON_STARTUP=true`, the app also attempts table creation on startup. Alembic migrations are still the cleaner approach for normal development.

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The Vite dev server will print the local URL, typically `http://localhost:5173`.

## Tests

Backend tests use an in-memory SQLite database with `aiosqlite` and cover:

- auth and role restrictions
- admin bootstrap flow
- student CRUD
- admission flow
- payment notification approval flow
- manual payments
- student payment summaries

Run them from `backend/`:

```bash
python -m pytest tests -v
```

## Current gaps

- The frontend is not yet fully connected to the backend beyond admin login
- The login screen currently uses a fixed admin email in the request body and only takes the password from the form
- The backend default `.env` created for local development should be replaced with real secrets and real database credentials
- There is no root-level unified dev script yet for running frontend and backend together

## Notes

- The backend expects JSON login payloads, not form-encoded login requests
- The generic `POST /auth/login` route does not exist; admin and student logins are separate
- The project currently contains backend and frontend subprojects with their own local setup needs
