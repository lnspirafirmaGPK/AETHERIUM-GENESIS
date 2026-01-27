import os
import urllib.parse
import httpx
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from .schemas import IdentityProfile, TokenSet
import time
import config

class BaseAuthProvider(ABC):
    @abstractmethod
    def get_login_url(self, state: str) -> str:
        pass

    @abstractmethod
    async def exchange_code(self, code: str) -> Tuple[IdentityProfile, TokenSet]:
        pass

class MockAuthProvider(BaseAuthProvider):
    def get_login_url(self, state: str) -> str:
        # Direct redirect to callback with a fake code
        params = {
            "code": "mock_auth_code_123",
            "state": state
        }
        return f"{config.GOOGLE_REDIRECT_URI}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str) -> Tuple[IdentityProfile, TokenSet]:
        # Return fake user
        identity = IdentityProfile(
            provider="mock",
            sub="mock-traveler-123",
            email="traveler@logenesis.local",
            name="Logenesis Traveler",
            picture="https://via.placeholder.com/150"
        )
        tokens = TokenSet(
            access_token="mock_access_token",
            refresh_token="mock_refresh_token",
            expires_at=time.time() + 3600
        )
        return identity, tokens

class GoogleAuthProvider(BaseAuthProvider):
    DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    def __init__(self):
        self.client_id = config.GOOGLE_CLIENT_ID
        self.client_secret = config.GOOGLE_CLIENT_SECRET
        self.redirect_uri = config.GOOGLE_REDIRECT_URI
        self._config = None

    async def _get_config(self):
        if not self._config:
            async with httpx.AsyncClient() as client:
                resp = await client.get(self.DISCOVERY_URL)
                self._config = resp.json()
        return self._config

    def get_login_url(self, state: str) -> str:
        # We can hardcode the auth endpoint or fetch it. Hardcoding is faster for now but less robust.
        # Let's use standard endpoint.
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "scope": "openid email profile",
            "redirect_uri": self.redirect_uri,
            "state": state,
            "access_type": "offline", # For refresh token
            "prompt": "consent"
        }
        return f"{base_url}?{urllib.parse.urlencode(params)}"

    async def exchange_code(self, code: str) -> Tuple[IdentityProfile, TokenSet]:
        token_endpoint = "https://oauth2.googleapis.com/token"

        async with httpx.AsyncClient() as client:
            # 1. Exchange Code for Token
            token_resp = await client.post(token_endpoint, data={
                "code": code,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code"
            })
            token_resp.raise_for_status()
            token_data = token_resp.json()

            # 2. Get User Info
            # Google supports ID Token, but let's just hit userinfo endpoint for simplicity/clarity
            access_token = token_data["access_token"]
            userinfo_endpoint = "https://openidconnect.googleapis.com/v1/userinfo"

            user_resp = await client.get(userinfo_endpoint, headers={
                "Authorization": f"Bearer {access_token}"
            })
            user_resp.raise_for_status()
            user_data = user_resp.json()

            # Map to Schema
            identity = IdentityProfile(
                provider="google",
                sub=user_data.get("sub"),
                email=user_data.get("email"),
                name=user_data.get("name"),
                picture=user_data.get("picture")
            )

            tokens = TokenSet(
                access_token=access_token,
                refresh_token=token_data.get("refresh_token"),
                expires_at=time.time() + token_data.get("expires_in", 3600)
            )

            return identity, tokens

def get_auth_provider() -> BaseAuthProvider:
    if config.AUTH_PROVIDER == "google":
        return GoogleAuthProvider()
    return MockAuthProvider()
