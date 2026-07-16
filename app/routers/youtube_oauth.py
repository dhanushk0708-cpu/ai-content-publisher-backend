from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from app.services.youtube.oauth_service import OAuthService

router = APIRouter(
    prefix="/youtube",
    tags=["YouTube OAuth"],
)

oauth = OAuthService()


@router.get("/connect")
def connect():

    try:
        authorization_url = oauth.get_authorization_url()

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    return RedirectResponse(
        url=authorization_url,
        status_code=307,
    )


@router.get("/callback")
def callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
):

    if error:
        raise HTTPException(
            status_code=400,
            detail=f"Google OAuth failed: {error}",
        )

    if not code:
        raise HTTPException(
            status_code=400,
            detail="Missing authorization code",
        )

    try:
        return oauth.exchange_code(
            code=code,
            state=state,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc
