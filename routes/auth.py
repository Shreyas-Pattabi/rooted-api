from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from schemas import UserLogin
from util.auth import (create_access_token, 
                       get_user_by_identifier)
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
    # refresh_token = await create_refresh_token(str(user.id))

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    # response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="Lax", secure=True)
    return response

# @router.post("/refresh")
# async def refresh_access_token(request: Request):
#     refresh_token = request.cookies.get("refresh_token")
#     if not refresh_token:
#         raise HTTPException(status_code=401, detail="Refresh token missing")

#     user_id = get_user_id_from_refresh_token(refresh_token)  # Extract user ID
#     if not await verify_refresh_token(user_id, refresh_token):
#         raise HTTPException(status_code=401, detail="Invalid refresh token")

#     new_access_token = create_access_token({"sub": user_id})
#     return {"access_token": new_access_token, "token_type": "bearer"}

# @router.post("/logout")
# async def logout(current_user: User = Depends(get_current_user)):
#     user_id = current_user.id
#     await revoke_refresh_token(user_id)
#     response = JSONResponse(content={"message": "Logged out successfully"})
#     response.delete_cookie("refresh_token")
#     return response