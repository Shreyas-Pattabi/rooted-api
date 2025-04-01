from datetime import datetime
from typing import Annotated, Optional, Union
from uuid import UUID

from pydantic import BaseModel, EmailStr, constr

PhoneStr = Annotated[str, constr(pattern=r'^\+?\d{10,15}$')]
Password = Annotated[str, constr(min_length=8, max_length=100)]
Identifier = Union[EmailStr, PhoneStr]

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneStr] = None 
    profile_picture: Optional[str] = None

class UserCreate(UserBase):
    password: Password

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneStr] = None 
    profile_picture: Optional[str] = None
    
class UserResponse(UserBase):
    id: UUID
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    identifier: Identifier  # Can be email or phone number
    password: Password


# Plant Schemas
class PlantBase(BaseModel):
    name: str
    type: Optional[str] = None
    water: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    image: Optional[str] = None 
    
class PlantUpdate(PlantBase):
    name: Optional[str] = None

class PlantResponse(PlantBase):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    last_watered: Optional[datetime] = None

    class Config:
        from_attributes = True