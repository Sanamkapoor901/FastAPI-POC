from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from user.crud import get_user_by_email, create_user, get_user_by_username
from utils import verify_password, create_access_token
from user.schemas import UserCreate, UserResponse
from dependencies import get_current_user
from user.models import User
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    user_by_username = get_user_by_username(db, username=user.username)
    if db_user or user_by_username:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return create_user(db, user=user)


@router.post("/login/", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/profile/", response_model=UserResponse)
async def read_users_profile(current_user: User = Depends(get_current_user)):
    return current_user