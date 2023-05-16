"""
Manages database connections and sessions.
"""

from models import get_session, User
from core.config import config
from schemas import UserBase, User
from datetime import datetime
from uuid import uuid4
from fastapi import HTTPException, status


# ----------------------
# User functions
# ----------------------
def get_user_by_email(email: str, name: str) -> User:
    with get_session() as session:
        user = session.query(User).filter_by(email=email, name=name).first()
        return user


def delete_user(email: str, uuid: str) -> bool:
    with get_session() as session:
        user = session.query(User).filter_by(email=email, uuid=uuid).first()
        if user:
            user.status = "deleted"
            session.commit()
            return True
        else:
            return False


def create_user(user: UserBase) -> User:
    _user = get_user_by_email(user.email, user.name)
    if _user:
        # TODO for now
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exist")
    with get_session() as session:
        new_user = User(
            uuid=uuid4(),
            name=user.name,
            email=user.email,
            created_at=datetime.now(),
            tokens=user.tokens,
            price=5.56,
            status="active"
        )
        session.add(new_user)
        session.commit()
        return new_user
