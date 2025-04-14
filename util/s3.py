from main import s3_client
from fastapi import UploadFile, HTTPException
from util.config import S3_BUCKET_NAME


def upload_to_s3(file: UploadFile, filename: str):
    try:
        # Upload without setting the object as public since we're blocking public access
        s3_client.upload_fileobj(
            file.file,
            S3_BUCKET_NAME,
            filename,
            ExtraArgs={"ContentType": file.content_type}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3: " + str(e))
