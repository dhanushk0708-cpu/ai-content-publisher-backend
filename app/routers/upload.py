from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.auth.dependencies import verify_token
from app.exceptions import DownloadError
from app.schemas.upload_schema import UploadRequest
from app.services.upload_service import UploadService

router = APIRouter()

upload_service = UploadService()


@router.post("/upload")
def upload(
    request: UploadRequest,
    user=Depends(verify_token),
):

    try:
        return upload_service.process_upload(str(request.instagram_url))

    except DownloadError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
