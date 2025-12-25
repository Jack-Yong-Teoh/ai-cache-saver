from typing import Optional
from sqlalchemy import BinaryExpression, ColumnOperators, func
from sqlalchemy.orm import Session
from app.models.databases.orm.user import User
from app.models.exceptions.not_found_exception import NotFoundException


def get_user_filter_criterion(
    user_id: int = None,
    email: str = None,
    is_active: bool = None,
    get_one: bool = True,
) -> list[BinaryExpression]:
    criterion = [
        (None if user_id is None else ColumnOperators.__eq__(User.id, user_id)),
        (
            None
            if email is None
            else ColumnOperators.__eq__(func.lower(User.email), func.lower(email))
        ),
        (
            None
            if is_active is None
            else ColumnOperators.__eq__(User.is_active, is_active)
        ),
    ]
    criterion = [x for x in criterion if x is not None]
    if get_one and len(criterion) == 0:
        raise ValueError("No filtering criteria provided")
    return criterion


def get_user(
    db: Session,
    user_id: int = None,
    email: str = None,
    optional: bool = False,
) -> Optional[User]:
    criterion = get_user_filter_criterion(user_id=user_id, email=email)
    db_user = db.query(User).filter(*criterion).one_or_none()

    if db_user is None and not optional:
        raise NotFoundException(
            "USER_NOT_FOUND", extra={"user_id": user_id, "email": email}
        )
    return db_user


def save_user(db: Session, user: User, auto_commit: bool = True) -> User:
    db.add(user)
    db.commit() if auto_commit else db.flush()
    db.refresh(user)
    return user
