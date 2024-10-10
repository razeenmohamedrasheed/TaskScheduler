from fastapi import APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from src.models.user_models import user
from typing import List
from fastapi.params import Depends
from src.db import get_db,SessionLocal,engine
from src.schemas import schemas
from passlib.context import CryptContext

router = APIRouter(
    tags=["User Management"]
)

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

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
