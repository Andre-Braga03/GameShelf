from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app.schemas import Token, UserCreate, UserLogin, UserRead
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
        if len(payload.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long."
            )
        exists = db.query(User).filter(User.email == payload.email).first()
        if exists:
            raise HTTPException(
                status_code=409,
                detail="User already exists."
            )
        
        user = User(
            email=payload.email,
            hashed_password=hash_password(payload.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return Token(access_token=create_access_token(user.id))

@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) :
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )
    return Token(access_token=create_access_token(user.id))


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) :
    return current_user
