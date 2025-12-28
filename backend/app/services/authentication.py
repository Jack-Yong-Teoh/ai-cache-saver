from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utilities.postgresql import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.queries.user import get_user
from app.models.databases.orm.user import User
import os

# Ensure bcrypt is the explicit scheme
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = os.environ.get("JWT_ALGORITHM")
security = HTTPBearer()


def hash_password(password: str) -> str:
    """Hashes password with strict 71-byte limit to prevent bcrypt crashes."""
    if not password:
        raise ValueError("Password cannot be empty")

    # Bcrypt max length is 72 bytes. We use 71 to be safe against null-terminator overhead.
    pwd_bytes = password.encode("utf-8")
    if len(pwd_bytes) > 71:
        password = pwd_bytes[:71].decode("utf-8", errors="ignore")

    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies password with the same 71-byte limit."""
    if not plain_password or not hashed_password:
        return False

    pwd_bytes = plain_password.encode("utf-8")
    if len(pwd_bytes) > 71:
        plain_password = pwd_bytes[:71].decode("utf-8", errors="ignore")

    try:
        return PWD_CONTEXT.verify(plain_password, hashed_password)
    except Exception:
        # Prevents 500 error if DB hash is malformed
        return False


def create_tokens(user_id: int) -> tuple[str, str]:
    if not SECRET_KEY or not ALGORITHM:
        raise RuntimeError("JWT Environment variables are missing")

    access_expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    access_token = jwt.encode(
        {"sub": str(user_id), "exp": access_expire, "type": "access"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    refresh_expire = datetime.now(timezone.utc) + timedelta(days=7)
    refresh_token = jwt.encode(
        {"sub": str(user_id), "exp": refresh_expire, "type": "refresh"},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return access_token, refresh_token


def decode_token(token: str, expected_type: str = "access") -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {expected_type}.",
            )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing user identification",
            )
        return int(user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


def decode_refresh_token(token: str) -> int:
    return decode_token(token, expected_type="refresh")

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
) -> User:
    """
    1. Swagger/Frontend sends 'Authorization: Bearer <token>'
    2. HTTPBearer extracts the <token> part into credentials.credentials
    3. We decode and verify it.
    """
    token = credentials.credentials
    
    # This calls your service logic (Signature check, Expiry check)
    user_id = decode_token(token, expected_type="access")
    
    user = get_user(db, user_id=user_id, optional=True)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
