from pathlib import Path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class YouTubeAuth:
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    def authenticate(self):

        token_path = Path("token.pickle")

        credentials = None

        # Load saved token
        if token_path.exists():
            with open(token_path, "rb") as token:
                credentials = pickle.load(token)

        # Refresh expired token
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # First login
        elif not credentials or not credentials.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", self.SCOPES
            )

            credentials = flow.run_local_server(port=0)

            # Save token
            with open(token_path, "wb") as token:
                pickle.dump(credentials, token)

        return credentials
