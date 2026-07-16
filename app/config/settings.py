import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    GEMINI_FALLBACK_MODELS = [
        GEMINI_MODEL,
        "gemini-2.5-flash-lite",
        "gemini-2.5-pro",
        "gemini-2.0-flash",
    ]

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")

    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    JWT_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 1440

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

    GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")


settings = Settings()
