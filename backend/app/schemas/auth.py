from pydantic import BaseModel, Field

from app.schemas.common import UserOut


class LoginRequest(BaseModel):
    email: str = Field(description="Email address used for login.")
    password: str = Field(min_length=6, description="Plain-text password with at least 6 characters.")


class AdminRegisterRequest(BaseModel):
    email: str = Field(description="Admin email address used for login.")
    full_name: str = Field(description="Display name of the admin user.")
    password: str = Field(min_length=6, description="Plain-text password with at least 6 characters.")


class AdminRegisterResponse(BaseModel):
    """Response returned after a successful admin registration."""

    user: UserOut


class TokenResponse(BaseModel):
    """JWT bearer token response for admin or student login."""

    access_token: str
    token_type: str = "bearer"
