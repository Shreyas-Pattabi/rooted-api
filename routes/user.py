from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import asyncio
from models import User
from schemas import UserBase, UserCreate, UserResponse, UserUpdate
from util.auth import get_current_user, get_user_by_identifier, hash_password
from util.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        if not user.email and not user.phone_number:
            raise HTTPException(status_code=400, detail="Either email or phone number is required.")
        
        if not user.password:
            raise HTTPException(status_code=400, detail="Password is required")
    
        # Check if the email is already registered (if provided)
        if user.email:
            existing_email = await get_user_by_identifier(db, user.email)  # Await the async function
            if existing_email:
                raise HTTPException(status_code=400, detail="Email already registered")

        # Check if the phone number is already registered (if provided)
        if user.phone_number:
            existing_phone = await get_user_by_identifier(db, user.phone_number)  # Await the async function
            if existing_phone:
                raise HTTPException(status_code=400, detail="Phone number already registered")

        # Hash the password before storing
        hashed_password = await asyncio.to_thread(hash_password, user.password) if user.password else None
    
        # Create a new user instance
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email if user.email else None,
            phone_number=user.phone_number if user.phone_number else None,
            profile_picture=user.profile_picture,
            hashed_password=hashed_password
        )

        # Save to the database
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user
    except HTTPException as e:
        raise e 

@router.get("/me", response_model=UserResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Returns the authenticated user's profile"""
    return current_user

@router.put("/me", response_model=UserBase)
async def update_user_profile(user_update: UserUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Updates the authenticated user's profile"""
    if user_update.email and user_update.email != current_user.email:
        existing_user = await db.execute(select(User).filter(User.email == user_update.email))  # Async query
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email is already in use")
    
    if user_update.phone_number and user_update.phone_number != current_user.phone_number:
        existing_user = await db.execute(select(User).filter(User.phone_number == user_update.phone_number))  # Async query
        existing_user = existing_user.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Phone number is already in use")
        
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)

    await db.commit()
    await db.refresh(current_user)

    return current_user