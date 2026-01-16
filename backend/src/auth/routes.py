"""Authentication routes"""
from fastapi import APIRouter, HTTPException, status, Response, Depends
from pydantic import BaseModel, EmailStr
from sqlmodel import Session as DBSession, select
from src.database.models import User, UserSession
from src.database.config import engine
from src.auth.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    generate_session_token
)
from src.auth.dependencies import get_current_user, get_optional_user
from datetime import datetime, timedelta
from typing import Optional

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class SigninRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime


class AuthResponse(BaseModel):
    user: UserResponse
    token: str


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, response: Response):
    """Sign up a new user"""
    with DBSession(engine) as session:
        # Check if user already exists
        statement = select(User).where(User.email == request.email)
        existing_user = session.exec(statement).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(request.password)
        user = User(
            email=request.email,
            name=request.name,
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        
        # Create session token
        session_token = generate_session_token()
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        user_session = UserSession(
            user_id=user.id,
            token=session_token,
            expires_at=expires_at
        )
        session.add(user_session)
        session.commit()
        
        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # Set session cookie
        response.set_cookie(
            key="session",
            value=session_token,
            httponly=True,
            max_age=30 * 24 * 60 * 60,  # 30 days
            samesite="lax",
            secure=True  # Set to True in production with HTTPS
        )
        
        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at
            ),
            token=access_token
        )


@router.post("/signin", response_model=AuthResponse)
async def signin(request: SigninRequest, response: Response):
    """Sign in an existing user"""
    with DBSession(engine) as session:
        # Find user
        statement = select(User).where(User.email == request.email)
        user = session.exec(statement).first()
        
        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Create session token
        session_token = generate_session_token()
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        user_session = UserSession(
            user_id=user.id,
            token=session_token,
            expires_at=expires_at
        )
        session.add(user_session)
        session.commit()
        
        # Create JWT token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # Set session cookie
        response.set_cookie(
            key="session",
            value=session_token,
            httponly=True,
            max_age=30 * 24 * 60 * 60,  # 30 days
            samesite="lax",
            secure=True  # Set to True in production with HTTPS
        )
        
        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                created_at=user.created_at
            ),
            token=access_token
        )


@router.get("/session", response_model=Optional[UserResponse])
async def get_session(user: Optional[User] = Depends(get_optional_user)):
    """Get current session user"""
    if not user:
        return None
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at
    )


@router.post("/signout")
async def signout(
    response: Response,
    user: Optional[User] = Depends(get_optional_user)
):
    """Sign out current user"""
    if user:
        with DBSession(engine) as session:
            # Delete all sessions for this user
            statement = select(UserSession).where(UserSession.user_id == user.id)
            sessions = session.exec(statement).all()
            for user_session in sessions:
                session.delete(user_session)
            session.commit()
    
    # Clear session cookie
    response.delete_cookie(key="session")
    
    return {"message": "Signed out successfully"}