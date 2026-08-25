from uuid import UUID, uuid4

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.functions.database import get_user_by_email_rq, create_user_rq
from app.functions.security import create_jwt
from app.models.user import User
from app.schemas.user import CommonUserRequest, CreateUserResponse, AuthUserResponse

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)

@router.post("/register", response_model=CreateUserResponse)
async def create_user(user: CommonUserRequest, session: AsyncSession = Depends(get_session)) -> CreateUserResponse:
    existing_user = await get_user_by_email_rq(session, user.email)

    if existing_user != None:
        raise HTTPException(
            status_code=409,
            detail="User with this email already exists.",
        )

    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = await create_user_rq(session, user.email, password_hash)

    return CreateUserResponse(
        id=new_user.id,
        email=new_user.email
    )

@router.post("/auth", response_model=AuthUserResponse)
async def auth_user(user: CommonUserRequest, session: AsyncSession = Depends(get_session)) -> AuthUserResponse:
    existing_user = await get_user_by_email_rq(session, user.email)

    if existing_user == None:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist.",
        )

    if not bcrypt.checkpw(user.password.encode('utf-8'), existing_user.password_hash.encode('utf-8')):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password.",
        )

    return AuthUserResponse(
        id=existing_user.id,
        email=existing_user.email,
        jwt=create_jwt(existing_user.id)
    )