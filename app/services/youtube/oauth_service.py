import os
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlencode

import requests
from jose import JWTError
from jose import jwt

from app.config.settings import settings
from app.services.youtube.youtube_auth import YouTubeAuth


class OAuthService:
    AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_URL = "https://oauth2.googleapis.com/token"

    def __init__(self):

        self.auth = YouTubeAuth()

    def _generate_state_token(self) -> str:

        if not settings.JWT_SECRET_KEY:
            raise RuntimeError(
                "JWT_SECRET_KEY is required to generate the Google OAuth state token."
            )

        payload = {
            "purpose": "youtube_oauth",
            "exp": datetime.utcnow() + timedelta(minutes=10),
            "iat": datetime.utcnow(),
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    def _validate_state_token(
        self,
        state: str | None,
    ):

        if not state:
            raise ValueError("Missing OAuth state")

        try:
            payload = jwt.decode(
                state,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )

        except JWTError as exc:
            raise ValueError("Invalid or expired OAuth state") from exc

        if payload.get("purpose") != "youtube_oauth":
            raise ValueError("Invalid OAuth state")

    def _persist_refresh_token(
        self,
        refresh_token: str,
    ) -> bool:

        settings.GOOGLE_REFRESH_TOKEN = refresh_token
        os.environ["GOOGLE_REFRESH_TOKEN"] = refresh_token

        env_path = Path(__file__).resolve().parents[3] / ".env"
        line = f"GOOGLE_REFRESH_TOKEN={refresh_token}"

        try:
            if env_path.exists():
                lines = env_path.read_text(encoding="utf-8").splitlines()
            else:
                lines = []

            replaced = False
            updated_lines = []

            for existing_line in lines:
                if existing_line.startswith("GOOGLE_REFRESH_TOKEN="):
                    updated_lines.append(line)
                    replaced = True
                else:
                    updated_lines.append(existing_line)

            if not replaced:
                updated_lines.append(line)

            env_path.write_text(
                "\n".join(updated_lines).strip() + "\n",
                encoding="utf-8",
            )

            return True

        except OSError:
            return False

    def get_authorization_url(self) -> str:

        self.auth.ensure_oauth_client_configured()

        state = self._generate_state_token()

        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "access_type": "offline",
            "prompt": "consent",
            "include_granted_scopes": "true",
            "scope": " ".join(self.auth.SCOPES),
            "state": state,
        }

        url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"

        print("\n")
        print("=" * 100)
        print("GOOGLE AUTH URL")
        print(url)
        print("=" * 100)
        print("\n")

        return url

    def exchange_code(
        self,
        code: str,
        state: str | None,
    ):

        self.auth.ensure_oauth_client_configured()
        self._validate_state_token(state)

        response = requests.post(
            self.TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
            timeout=30,
        )

        payload = response.json()

        if not response.ok:
            raise RuntimeError(
                payload.get(
                    "error_description",
                    payload.get("error", "Google OAuth failed"),
                )
            )

        refresh_token = payload.get("refresh_token") or settings.GOOGLE_REFRESH_TOKEN

        if not refresh_token:
            raise RuntimeError("Google did not return a refresh token.")

        stored_to_env_file = self._persist_refresh_token(refresh_token)

        return {
            "success": True,
            "message": "Google OAuth completed successfully.",
            "refresh_token_configured": True,
            "stored_to_env_file": stored_to_env_file,
            "scope": payload.get(
                "scope",
                " ".join(self.auth.SCOPES),
            ),
        }
