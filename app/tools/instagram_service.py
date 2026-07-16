from pathlib import Path

import yt_dlp

from app.exceptions import DownloadError


class InstagramService:
    def download_reel(self, instagram_url: str):

        try:
            output_dir = Path("storage/videos")
            output_dir.mkdir(parents=True, exist_ok=True)

            output_template = str(output_dir / "%(id)s.%(ext)s")

            options = {
                "outtmpl": output_template,
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "quiet": True,
            }

            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(instagram_url, download=True)

                filename = ydl.prepare_filename(info)

                return {
                    "success": True,
                    "video_path": filename,
                    "metadata": {
                        "title": info.get("title"),
                        "description": info.get("description"),
                        "uploader": info.get("uploader"),
                        "duration": info.get("duration"),
                        "thumbnail": info.get("thumbnail"),
                        "upload_date": info.get("upload_date"),
                        "webpage_url": info.get("webpage_url"),
                    },
                }

        except Exception as e:
            raise DownloadError(str(e))
