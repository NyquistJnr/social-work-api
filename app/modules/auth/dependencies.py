import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.user.entity import User, UserTypeEnum
from app.modules.user.repository import UserRepository

_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        if payload.get("type") != "access":
            raise unauthorized
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        raise unauthorized

    user = await UserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        raise unauthorized

    return user


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    if credentials is None:
        return None

    try:
        payload = decode_access_token(credentials.credentials)
        if payload.get("type") != "access":
            return None
        user_id = uuid.UUID(payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        return None

    user = await UserRepository(db).get_by_id(user_id)
    if user is None or not user.is_active:
        return None

    return user



async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return current_user


async def get_current_admin_or_instructor(current_user: User = Depends(get_current_user)) -> User:
    if current_user.user_type not in (UserTypeEnum.ADMIN, UserTypeEnum.INSTRUCTOR):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin or instructor access required")
    return current_user
