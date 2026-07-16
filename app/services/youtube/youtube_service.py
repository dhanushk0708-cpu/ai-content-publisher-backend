from pathlib import Path
from urllib.parse import urlparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from app.services.youtube.youtube_auth import YouTubeAuth


class YouTubeService:
    def __init__(self):

        self.auth = YouTubeAuth()
        self.backend_root = Path(__file__).resolve().parents[3]
        self.storage_root = (self.backend_root / "storage" / "videos").resolve()

    def _resolve_storage_video_path(
        self,
        filename: str,
    ) -> Path:

        resolved_path = (self.storage_root / Path(filename).name).resolve()

        try:
            resolved_path.relative_to(self.storage_root)
        except ValueError as exc:
            raise ValueError("Video path must remain inside storage/videos") from exc

        if not resolved_path.exists():
            raise FileNotFoundError(f"Video file not found: {resolved_path}")

        return resolved_path

    def resolve_video_path(
        self,
        video_path: str,
    ) -> Path:

        cleaned_path = video_path.strip()

        if not cleaned_path:
            raise ValueError("video_path is required")

        parsed = urlparse(cleaned_path)

        if parsed.scheme in {"http", "https"}:
            filename = Path(parsed.path).name

            if not filename:
                raise ValueError("Invalid video URL supplied for upload")

            return self._resolve_storage_video_path(filename)

        path = Path(cleaned_path)

        if not path.is_absolute():
            path = (self.backend_root / path).resolve()
        else:
            path = path.resolve()

        try:
            path.relative_to(self.storage_root)
        except ValueError as exc:
            raise ValueError("Only files inside storage/videos can be uploaded") from exc

        if not path.exists():
            raise FileNotFoundError(f"Video file not found: {path}")

        return path

    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: list[str],
        privacy: str,
        category: str,
    ):

        resolved_video_path = self.resolve_video_path(video_path)
        credentials = self.auth.get_authenticated_credentials()

        youtube = build(
            "youtube",
            "v3",
            credentials=credentials,
        )

        request = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": str(category),
                },
                "status": {
                    "privacyStatus": privacy,
                },
            },
            media_body=MediaFileUpload(
                str(resolved_video_path),
                resumable=True,
            ),
        )

        try:
            response = request.execute()

        except HttpError as exc:
            raise RuntimeError(
                f"YouTube upload failed: {exc}"
            ) from exc

        video_id = response["id"]

        return {
            "success": True,
            "video_id": video_id,
            "url": f"https://youtube.com/watch?v={video_id}",
        }
