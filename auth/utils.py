# app/auth/utils.py  (refactored)

import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os

# ── Settings ──────────────────────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# ── Password hashing helpers ─────────────────────────────────────────
def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.
    Returns bytes ⇒ decode to str for DB storage.
    """
    salt = bcrypt.gensalt()                     # 12-round salt by default
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()                      # store as UTF-8 string


def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a plaintext password against a stored bcrypt hash.
    """
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except ValueError:                          # if hash format is wrong
        return False

# ── JWT helpers ───────────────────────────────────────────────────────
def create_access_token(data: dict,
                        expires_delta: timedelta | None = None) -> str:
    """
    Generate a signed JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
