from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.auth.dependencies import verify_token
from app.schemas.youtube_schema import YouTubeUploadRequest
from app.services.youtube.youtube_service import YouTubeService

router = APIRouter(
    tags=["YouTube"],
)


@router.post("/youtube/upload")
def upload_video(
    request: YouTubeUploadRequest,
    user=Depends(verify_token),
):

    try:
        youtube = YouTubeService()

        return youtube.upload_video(
            video_path=request.video_path,
            title=request.title,
            description=request.description,
            tags=request.hashtags,
            privacy=request.privacy,
            category=request.category,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
