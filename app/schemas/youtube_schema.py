from pydantic import BaseModel
from pydantic import Field


class YouTubeUploadRequest(BaseModel):
    video_path: str

    title: str

    description: str

    hashtags: list[str] = Field(default_factory=list)

    privacy: str

    category: str
