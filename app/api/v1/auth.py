from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.auth.models import AuthUser
from app.auth.schemas import UserRegister, UserLogin, Token, UserResponse
from app.auth.jwt import create_access_token, get_current_active_user
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(AuthUser).filter(
        or_(AuthUser.email == user_data.email, AuthUser.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this email or username already exists"
        )
    
    # Create new user
    hashed_password = AuthUser.hash_password(user_data.password)
    new_user = AuthUser(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Find user by username or email
    user = db.query(AuthUser).filter(
        or_(AuthUser.username == form_data.username, AuthUser.email == form_data.username)
    ).first()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: AuthUser = Depends(get_current_active_user)):
    return current_user

@router.post("/logout")
def logout(current_user: AuthUser = Depends(get_current_active_user)):
    # In a stateless JWT system, logout is handled client-side
    # This endpoint can be used for audit logging
    return {"message": "Successfully logged out"}