from fastapi import APIRouter

from app.schemas.youtube_schema import YouTubeUploadRequest
from app.services.youtube.youtube_service import YouTubeService

router = APIRouter()


@router.post("/youtube/upload")
def upload_video(request: YouTubeUploadRequest):

    youtube = YouTubeService()

    return youtube.upload_video(
        video_path=request.video_path,
        title=request.title,
        description=request.description,
        tags=request.hashtags,
        privacy=request.privacy,
        category=request.category,
    )
