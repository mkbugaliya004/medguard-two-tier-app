import hashlib
import hmac
import os
import secrets
import time

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Fixed demonstration account requested for this development project.
# Override these values with environment variables when needed.
ADMIN_USERNAME = os.getenv("MEDGUARD_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("MEDGUARD_ADMIN_PASSWORD", "admin1")
SESSION_SECRET = os.getenv("MEDGUARD_SESSION_SECRET", "development-only-change-this-secret")
COOKIE_NAME = "medguard_session"
SESSION_TTL_SECONDS = 8 * 60 * 60


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)


def _sign(payload: str) -> str:
    digest = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{digest}"


def _valid_session(value: str | None) -> bool:
    if not value or "." not in value:
        return False
    payload, supplied_signature = value.rsplit(".", 1)
    expected_signature = hmac.new(
        SESSION_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(supplied_signature, expected_signature):
        return False
    try:
        username, expires = payload.rsplit(":", 1)
        return username == ADMIN_USERNAME and int(expires) > int(time.time())
    except (ValueError, TypeError):
        return False


def require_login(request: Request) -> None:
    if not _valid_session(request.cookies.get(COOKIE_NAME)):
        raise HTTPException(status_code=401, detail="Please log in to continue.")


@router.post("/login")
def login(data: LoginRequest, response: Response):
    username_ok = hmac.compare_digest(data.username, ADMIN_USERNAME)
    password_ok = hmac.compare_digest(data.password, ADMIN_PASSWORD)
    if not (username_ok and password_ok):
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    expires = int(time.time()) + SESSION_TTL_SECONDS
    token = _sign(f"{ADMIN_USERNAME}:{expires}")
    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        samesite="lax",
        max_age=SESSION_TTL_SECONDS,
        path="/",
    )
    return {"authenticated": True, "username": ADMIN_USERNAME, "role": "admin"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key=COOKIE_NAME, path="/")
    return {"authenticated": False}


@router.get("/me")
def current_user(request: Request):
    require_login(request)
    return {"authenticated": True, "username": ADMIN_USERNAME, "role": "admin"}
