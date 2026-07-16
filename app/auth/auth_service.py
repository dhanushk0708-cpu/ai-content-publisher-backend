from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token
from app.config.settings import settings


class AuthService:
    def login(
        self,
        username: str,
        password: str,
    ):

        admin_username = settings.ADMIN_USERNAME

        admin_password_hash = settings.ADMIN_PASSWORD_HASH

        if username != admin_username:
            return None

        if not verify_password(
            password,
            admin_password_hash,
        ):
            return None

        access_token = create_access_token(
            {
                "sub": username,
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
