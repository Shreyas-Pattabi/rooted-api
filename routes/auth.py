from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import UserLogin
from util.auth import (create_access_token, 
                       get_user_by_identifier,
                       get_current_user)
from util.database import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_identifier(db, user_data.identifier)
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    access_token = create_access_token({"sub": str(user.id)})

    response = JSONResponse(content={"access_token": access_token, 
                                     "token_type": "bearer", 
                                     "user" : {"first_name": user.first_name, 
                                                "last_name": user.last_name, 
                                                "email": user.email, 
                                                "profile_picture": user.profile_picture,
                                                "created_at": user.created_at.strftime("%B %Y")}})
    return response

@router.get("/verify")
def verify_token(current_user: User = Depends(get_current_user)):
    return {"message": "Token is valid"}