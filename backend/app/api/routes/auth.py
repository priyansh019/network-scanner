from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.model.db_user import User
from app.model.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

@router.post("/auth/register", response_model=TokenResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user and return a JWT token."""
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticate an existing user and return a JWT token."""
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/token")
def login_for_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}