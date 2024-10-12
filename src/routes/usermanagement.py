from fastapi import APIRouter,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.models.user_models import user,login
from typing import List
from fastapi.params import Depends
from jose import JWTError, jwt
from src.db import get_db,SessionLocal,engine
from src.schemas import schemas
from passlib.context import CryptContext
from datetime import timedelta, datetime,timezone

router = APIRouter(
    tags=["User Management"]
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = "f782a15248f4ce2a9f4614ce16e6ce4d586ba18516c9c7210fb00c40b46b62d6" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  

@router.post('/user',status_code=status.HTTP_201_CREATED)
async def signUp(payload:user,db:Session = Depends(get_db)):
    try:
        hashedPassword = pwd_context.hash(payload.password)
        new_user = schemas.Users(
            role_id=payload.role_id,
            username=payload.username,
            email=payload.email,
            contact=payload.contact,
            password=hashedPassword
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message":"Created User"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the task.")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(schemas.Users).filter(schemas.Users.username == payload.username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if not verify_password(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
             data={"sub": user.username, "role_id": user.role_id,"user_id":user.userid,"email":user.email}, 
            expires_delta=access_token_expires
        )

        return {
            "message": "Login successful",
            "user_id": user.userid,
            "role_id": user.role_id,
            "access_token": access_token
        }
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during login")