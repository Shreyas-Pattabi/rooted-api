#upload.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from util.config import S3_BUCKET_NAME, AWS_REGION, PLANT_NET_API_KEY
from util.s3 import upload_to_s3
from uuid import uuid4
import os
import requests

router = APIRouter()

@router.post("/")
async def upload(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
    
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    
    # Upload the image to S3
    upload_to_s3(file, unique_filename)
    
    public_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{unique_filename}"
    return JSONResponse({
        "filename": unique_filename,
        "url": public_url
    })

@router.post("/recognize")
async def upload_and_recognize(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")
    
    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4().hex}{ext}"
    
    # Upload the image to S3
    upload_to_s3(file, unique_filename)
    
    public_url = f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{unique_filename}"
    request_url = (
        f"https://my-api.plantnet.org/v2/identify/all?"
        f"images={public_url}"
        f"&organs=auto"
        f"&include-related-images=false"
        f"&no-reject=false"
        f"&nb-results=1"
        f"&lang=en"
        f"&type=kt"
        f"&api-key={PLANT_NET_API_KEY}"
    )
    header = {"Content-Type": "application/json"}

    response = requests.get(request_url, headers=header)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    data = response.json()
    results = data.get("results", [])

    # Initialize fields in case results is empty
    scientific_name = None
    common_name = None
    
    if results:
        first_result = results[0]
        species = first_result.get("species", {})
        scientific_name = species.get("scientificName")
        common_names = species.get("commonNames", [])
        if common_names:
            common_name = common_names[0]

    return JSONResponse({
        "filename": unique_filename,
        "url": public_url,
        "name": common_name,
        "type": scientific_name
    })