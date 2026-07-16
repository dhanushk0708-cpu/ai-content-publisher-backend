from pydantic import BaseModel


class YouTubeUploadRequest(BaseModel):
    video_path: str

    title: str

    description: str

    hashtags: list[str]

    privacy: str

    category: str
