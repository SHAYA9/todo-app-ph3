"""Authentication dependencies for FastAPI"""
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session as DBSession, select
from typing import Optional
from src.database.models import User, UserSession
from src.database.config import engine
from src.auth.utils import verify_token
from datetime import datetime

security = HTTPBearer(auto_error=False)


async def get_current_user_from_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """Get current user from Bearer token"""
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = verify_token(token)
    
    if not payload:
        return None
    
    user_id = payload.get("sub")
    if not user_id:
        return None
    
    with DBSession(engine) as session:
        user = session.get(User, int(user_id))
        return user


async def get_current_user_from_cookie(
    session_token: Optional[str] = Cookie(None, alias="session")
) -> Optional[User]:
    """Get current user from session cookie"""
    if not session_token:
        return None
    
    with DBSession(engine) as db_session:
        # Find session
        statement = select(UserSession).where(
            UserSession.token == session_token,
            UserSession.expires_at > datetime.utcnow()
        )
        session_obj = db_session.exec(statement).first()
        
        if not session_obj:
            return None
        
        # Get user
        user = db_session.get(User, session_obj.user_id)
        return user


async def get_current_user(
    user_from_token: Optional[User] = Depends(get_current_user_from_token),
    user_from_cookie: Optional[User] = Depends(get_current_user_from_cookie)
) -> User:
    """Get current user from either token or cookie"""
    user = user_from_token or user_from_cookie
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    return user


async def get_optional_user(
    user_from_token: Optional[User] = Depends(get_current_user_from_token),
    user_from_cookie: Optional[User] = Depends(get_current_user_from_cookie)
) -> Optional[User]:
    """Get current user optionally (doesn't raise exception if not authenticated)"""
    return user_from_token or user_from_cookie