import uuid
from sqlalchemy import (Boolean, CheckConstraint, Column, DateTime, Float, Integer,
                        String, ForeignKey,func)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from util.database import Base

class User(Base):
    __tablename__ = "users"

    # Administrative fields
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # User Fields
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)  
    phone_number = Column(String, unique=True, index=True, nullable=True) 
    profile_picture = Column(String(255), nullable=True) 

    # Authentication fields
    hashed_password = Column(String, nullable=False)

    # Plants relationship
    plants = relationship("Plant", back_populates="user", cascade="all, delete")

    # Constraints
    __table_args__ = (
        CheckConstraint("email IS NOT NULL OR phone_number IS NOT NULL", name="must_have_contact"),
    )


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=True)
    water = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    image = Column(String, nullable=True)  # URL or path to image
    last_watered = Column(DateTime, nullable=True, default=None)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Foreign key to link plants to a user
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="plants") 

