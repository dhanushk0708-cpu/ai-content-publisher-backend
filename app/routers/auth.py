from fastapi import APIRouter, HTTPException

from app.auth.auth_service import AuthService
from app.schemas.login_schema import LoginRequest
from app.schemas.token_schema import TokenResponse

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
):

    token = auth_service.login(
        request.username,
        request.password,
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return token
