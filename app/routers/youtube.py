from fastapi import APIRouter
from fastapi import Depends

from app.auth.dependencies import verify_token

from app.schemas.youtube_schema import YouTubeUploadRequest
from app.services.youtube.youtube_service import YouTubeService

router = APIRouter()

youtube = YouTubeService()


@router.post("/youtube/upload")
def upload_video(
    request: YouTubeUploadRequest,
    user=Depends(verify_token),
):

    return youtube.upload_video(
        video_path=request.video_path,
        title=request.title,
        description=request.description,
        tags=request.hashtags,
        privacy=request.privacy,
        category=request.category,
    )
