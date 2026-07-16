from pydantic import BaseModel, HttpUrl


class UploadRequest(BaseModel):
    instagram_url: HttpUrl
