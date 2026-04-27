from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

# Import Utilities & Database
from app.utilities.postgresql import get_db
from app.queries.user import get_user, save_user
from app.models.databases.orm.user import User

# Import Services (The file above)
from app.services.authentication import (
    hash_password,
    verify_password,
    create_tokens,
    decode_refresh_token,
)

# Import Pydantic Schemas (From your base.py)
from app.models.pydantic_schemas.base import (
    SignupRequest,
    LoginRequest,
    RefreshRequest,
    TokenResponse,
)


async def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # 1. Check if email exists
    if get_user(db, email=payload.email, optional=True):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # 2. Hash Password (The service handles truncation now)
    hashed_pw = hash_password(payload.password)

    new_user = User(username=payload.username, email=payload.email, password=hashed_pw)

    save_user(db, new_user)

    # 3. Auto-Login (Optional)
    access_token, refresh_token = create_tokens(new_user.id)

    return {
        "message": "User created successfully",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = get_user(db, email=payload.email)

    # verify_password handles truncation safety
    if not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

    access_token, refresh_token = create_tokens(user.id)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        username=user.username,
        user_id=user.id,
    )


async def logout():
    return {"message": "Successfully logged out"}


async def refresh(payload: RefreshRequest):
    user_id = decode_refresh_token(payload.refresh_token)
    access_token, new_refresh_token = create_tokens(user_id)
    return TokenResponse(
        access_token=access_token, refresh_token=new_refresh_token, token_type="bearer"
    )
