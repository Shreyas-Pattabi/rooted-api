#upload.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from util.config import S3_BUCKET_NAME, AWS_REGION
from util.s3 import upload_to_s3
from uuid import uuid4
import os

router = APIRouter()

@router.post("/")
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
    
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    
    # Upload the image to S3
    upload_to_s3(file, unique_filename)
    
    # Generate a pre-signed URL for temporary access
    public_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
    return JSONResponse({
        "filename": unique_filename,
        "url": public_url
    })

# @router.post("/recognize")
# async def upload_and_recognize(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
    
#     ext = os.path.splitext(file.filename)[1]
#     unique_filename = f"{uuid4().hex}{ext}"
    
#     # Upload the image to S3
#     upload_to_s3(file, unique_filename)
    
#     # Generate a pre-signed URL for temporary access
#     public_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
#     pass