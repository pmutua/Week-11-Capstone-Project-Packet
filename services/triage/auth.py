# auth.py - Week 6 Monday, Lesson 5: the auth module every later service in
# this folder imports (secure_triage_api.py, and the Further Challenges).
# It is an assembly of things already run standalone earlier in the lesson:
#   - check_password()  is hash_demo.py's bcrypt.checkpw, wrapped around a
#                        small user table.
#   - create_token()     is token_demo.py's jwt.encode, with a realistic
#                        30-minute lifetime instead of 3 seconds.
#   - current_user()     is the one genuinely new piece: a FastAPI
#                        dependency (the "doorman") that decodes and
#                        verifies the Bearer token on every protected call.
#
# JWT_SECRET is read from .env (see repo-root .env.example) with a dev-only
# fallback so the file still runs for a first read-through without secrets
# configured — never rely on the fallback outside a classroom.

from __future__ import annotations

import os
import time

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "dev-only-secret-please-change-me-32chars!")
TOKEN_LIFETIME_SECONDS = 30 * 60  # 30 minutes

# Two demo users: "mercy" (coordinator, may triage) and "guest" (viewer,
# read-only — used by Further Challenge C, further_challenge_c_roles.py, to
# prove a valid token can still earn a 403). Passwords are hashed at import
# time; neither is ever stored or logged as plain text.
USERS: dict[str, dict[str, object]] = {
    "mercy": {
        "password_hash": bcrypt.hashpw(b"logistics2026", bcrypt.gensalt()),
        "role": "coordinator",
    },
    "guest": {
        "password_hash": bcrypt.hashpw(b"lookaround", bcrypt.gensalt()),
        "role": "viewer",
    },
}


def check_password(username: str, password: str) -> bool:
    user = USERS.get(username)
    if user is None:
        return False
    return bcrypt.checkpw(password.encode(), user["password_hash"])


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "role": USERS[username]["role"],
        "exp": int(time.time()) + TOKEN_LIFETIME_SECONDS,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


bearer = HTTPBearer()


def current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer)) -> dict:
    """FastAPI dependency: verifies the Bearer token before the endpoint runs.

    A missing token is rejected by HTTPBearer itself before this function is
    even called. A present-but-bad token (expired, or altered so its
    signature no longer matches) is turned into a clean 401 here, instead of
    letting jwt.decode's exception surface as an unhandled 500.
    """
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired. Log in again.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return payload
