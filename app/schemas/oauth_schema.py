from pydantic import BaseModel


class OAuthCallback(BaseModel):
    code: str
