import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, UserRegister


async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )

    return result.scalar_one_or_none()


async def register_user(
    db: AsyncSession,
    data: UserRegister,
) -> User:
    existing_user = await get_user_by_email(
        db,
        data.email,
    )

    if existing_user:
        raise ValueError("Email is already registered")

    user = User(
        id=uuid.uuid4(),
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
    )

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(
    db: AsyncSession,
    data: LoginRequest,
) -> User | None:
    user = await get_user_by_email(
        db,
        data.email,
    )

    if not user:
        return None

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        return None

    return user


async def create_user_token(
    db: AsyncSession,
    data: LoginRequest,
) -> str | None:
    user = await authenticate_user(db, data)

    if not user:
        return None

    return create_access_token(str(user.id))