from fastapi import APIRouter, Request, Response, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from itsdangerous import URLSafeTimedSerializer
from typing import Optional
import secrets
import config
import logging
from .providers import get_auth_provider
from .session_manager import AuthManager

logger = logging.getLogger("AuthRoutes")
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Initialize Managers
auth_manager = AuthManager()
signer = URLSafeTimedSerializer(config.SECRET_KEY, salt="logenesis-session")

COOKIE_NAME = "logenesis_session"

def get_current_user_id(request: Request) -> Optional[str]:
    """
    Extracts and validates the current User ID from the signed session cookie.

    Args:
        request: The incoming HTTP request containing cookies.

    Returns:
        Optional[str]: The user ID (sub) if valid, None otherwise.
    """
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return None
    try:
        # max_age=14 days
        user_id = signer.loads(cookie, max_age=86400 * 14)
        return user_id
    except Exception:
        return None

@router.get("/login")
def login(request: Request):
    """
    Initiates the OAuth 2.0 Authorization Code flow.
    Redirects the user to the configured Identity Provider's login page.

    Side Effects:
        - Generates a random CSRF state.
        - Sets an HTTP-only cookie `oauth_state` for CSRF validation.
    """
    provider = get_auth_provider()
    # Generate random state for CSRF protection
    state = secrets.token_urlsafe(16)

    # In a real app, store state in a cookie/session to verify later
    # For now, we trust the provider redirect

    auth_url = provider.get_login_url(state=state)
    response = RedirectResponse(url=auth_url)

    # Store state in cookie to verify on callback
    response.set_cookie(key="oauth_state", value=state, httponly=True)

    return response

@router.get("/callback")
async def callback(request: Request):
    """
    Handles the OAuth provider callback.
    Exchanges the authorization code for tokens and creates a session.

    Query Params:
        code (str): The authorization code.
        state (str): The returned CSRF state token.

    Returns:
        RedirectResponse: Redirects to the root application URL ('/') upon success.

    Raises:
        HTTPException(400): If code is missing or state is invalid (CSRF failure).
        HTTPException(500): If the token exchange fails.
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    stored_state = request.cookies.get("oauth_state")

    if not code:
        raise HTTPException(status_code=400, detail="Missing auth code")

    # CSRF Check
    # Mock provider might assume strict state handling or bypass
    if config.AUTH_PROVIDER != "mock" and state != stored_state:
        logger.warning("CSRF State mismatch")
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    provider = get_auth_provider()
    try:
        identity, tokens = await provider.exchange_code(code)
    except Exception as e:
        logger.error(f"Auth Exchange Failed: {e}")
        raise HTTPException(status_code=500, detail="Authentication failed")

    # Determine User ID
    user_id = identity.sub

    # Persist Session
    session = auth_manager.upsert_user(user_id, identity, tokens)

    # Create Signed Cookie
    signed_session_id = signer.dumps(user_id)

    # Redirect to App
    response = RedirectResponse(url="/") # Back to root
    response.set_cookie(
        key=COOKIE_NAME,
        value=signed_session_id,
        httponly=True,
        secure=False, # Set True in Prod with HTTPS
        samesite="lax",
        max_age=86400 * 14
    )
    response.delete_cookie("oauth_state")

    return response

@router.get("/me")
def get_me(request: Request):
    """
    Returns the current authenticated user's profile and cognitive state.
    Used by the frontend to verify session validity.

    Returns:
        JSONResponse:
            - { authenticated: True, user: ..., logenesis_state: ... }
            - { authenticated: False } (if no valid session)
    """
    user_id = get_current_user_id(request)
    if not user_id:
        return JSONResponse({"authenticated": False}, status_code=401)

    session = auth_manager.get_user(user_id)
    if not session:
         return JSONResponse({"authenticated": False}, status_code=401)

    return {
        "authenticated": True,
        "user": session.identity.model_dump(),
        "logenesis_state": session.logenesis_state.model_dump()
    }

@router.get("/logout")
def logout():
    """
    Terminates the user session by clearing the session cookie.
    Does not invalidate the OAuth Refresh Token on the backend (yet).
    """
    response = RedirectResponse(url="/")
    response.delete_cookie(COOKIE_NAME)
    return response
