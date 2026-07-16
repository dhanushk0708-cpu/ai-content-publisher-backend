from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.services.youtube.youtube_auth import YouTubeAuth


class YouTubeService:
    def __init__(self):

        auth = YouTubeAuth()

        credentials = auth.authenticate()

        self.youtube = build("youtube", "v3", credentials=credentials)

    def upload_video(self, video_path, title, description, tags, privacy, category):

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": category,
                },
                "status": {"privacyStatus": privacy},
            },
            media_body=MediaFileUpload(video_path, resumable=True),
        )

        response = request.execute()

        video_id = response["id"]

        return {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }
