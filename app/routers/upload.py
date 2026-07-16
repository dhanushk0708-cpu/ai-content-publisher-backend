from fastapi import APIRouter, HTTPException

from app.exceptions import DownloadError
from app.schemas.upload_schema import UploadRequest
from app.services.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.post("/upload")
def upload(request: UploadRequest):

    try:
        result = upload_service.process_upload(str(request.instagram_url))

        return result

    except DownloadError as e:
        raise HTTPException(status_code=400, detail=str(e))
