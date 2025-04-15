from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.sql import text

from util.config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY
from util.database import Base, engine, get_db
from simulation import simulate_plant_updates
import asyncio
import boto3

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables async
    
    task = asyncio.create_task(simulate_plant_updates())

    yield  # Application startup happens here
    await engine.dispose()  # Cleanup when app shuts down

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION 
)

from routes import auth, user, plant, upload

@app.get("/")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"message": "API is running", "database": "Connected"}
    except Exception as e:
        print(f"Database connection error: {e}")
        return {"message": "API is running", "database": "Error", "error": str(e)}

app.include_router(user.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")
app.include_router(plant.router, prefix="/plants")
app.include_router(upload.router, prefix="/upload")