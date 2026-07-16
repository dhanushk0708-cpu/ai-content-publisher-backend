from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from app.config.settings import settings


class YouTubeAuth:
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
    TOKEN_URI = "https://oauth2.googleapis.com/token"

    def ensure_oauth_client_configured(self):

        missing = []

        if not settings.GOOGLE_CLIENT_ID:
            missing.append("GOOGLE_CLIENT_ID")

        if not settings.GOOGLE_CLIENT_SECRET:
            missing.append("GOOGLE_CLIENT_SECRET")

        if not settings.GOOGLE_REDIRECT_URI:
            missing.append("GOOGLE_REDIRECT_URI")

        if missing:
            raise RuntimeError(
                "Missing Google OAuth configuration: "
                + ", ".join(missing)
            )

    def ensure_refresh_token_configured(self):

        self.ensure_oauth_client_configured()

        if not settings.GOOGLE_REFRESH_TOKEN:
            raise RuntimeError(
                "Google refresh token is not configured. "
                "Open /youtube/connect once to authorize the YouTube channel."
            )

    def build_credentials(
        self,
        access_token: str | None = None,
        refresh_token: str | None = None,
    ) -> Credentials:

        self.ensure_oauth_client_configured()

        resolved_refresh_token = refresh_token or settings.GOOGLE_REFRESH_TOKEN

        return Credentials(
            token=access_token,
            refresh_token=resolved_refresh_token,
            token_uri=self.TOKEN_URI,
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            scopes=self.SCOPES,
        )

    def get_authenticated_credentials(self) -> Credentials:

        self.ensure_refresh_token_configured()

        credentials = self.build_credentials()

        if not credentials.valid:
            credentials.refresh(Request())

        return credentials
