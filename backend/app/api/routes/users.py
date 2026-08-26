from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user, require_role
from app.models.user import User, UserRole
from app.schemas.auth import UserResponse


router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_my_profile(
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
):
    return current_user


@router.get(
    "/admin-test",
    response_model=UserResponse,
)
async def admin_test(
    current_user: Annotated[
        User,
        Depends(require_role(UserRole.ADMIN)),
    ],
):
    return current_user