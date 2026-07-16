from pathlib import Path

from app.services.seo_service import SEOService
from app.tools.instagram_service import InstagramService


class UploadService:
    def __init__(self):

        self.instagram = InstagramService()
        self.seo = SEOService()

    def process_upload(self, instagram_url: str):

        download_result = self.instagram.download_reel(instagram_url)

        seo_result = self.seo.generate(download_result["metadata"])

        filename = Path(download_result["video_path"]).name

        return {
            "success": True,
            "video": {
                "url": f"https://ai-content-publisher-backend.onrender.com/videos/{filename}",
                "thumbnail": download_result["metadata"]["thumbnail"],
                "duration": download_result["metadata"]["duration"],
            },
            "instagram": {
                "uploader": download_result["metadata"]["uploader"],
                "caption": download_result["metadata"]["description"],
                "upload_date": download_result["metadata"]["upload_date"],
            },
            "seo": seo_result,
        }
