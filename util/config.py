import os
from enum import Enum

from dotenv import load_dotenv

load_dotenv()

# Database Connection
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

# S3 Connection
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_REGION=os.getenv("AWS_REGION")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")

# API Keys
PLANT_NET_API_KEY=os.getenv("PLANT_NET_API_KEY")

# Token creation
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
