from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class IdentityProfile(BaseModel):
    """
    Standardized User Identity derived from OAuth provider.
    Anchored to the immutable 'sub' claim.
    """
    provider: str = Field(..., description="Provider name (e.g., google, mock)")
    sub: str = Field(..., description="Subject ID from Provider (Immutable Unique Identifier)")
    email: Optional[str] = Field(None, description="User email (Mutable attribute)")
    name: Optional[str] = Field(None, description="Display name")
    picture: Optional[str] = Field(None, description="Avatar URL")

class TokenSet(BaseModel):
    """
    Container for OAuth 2.0 tokens.
    """
    access_token: str = Field(..., description="Short-lived access token for API calls")
    refresh_token: Optional[str] = Field(None, description="Long-lived token for refreshing access")
    expires_at: float = Field(..., description="Unix timestamp of access token expiration")

class LogenesisStateSummary(BaseModel):
    """
    Lightweight summary of the cognitive state stored in the auth record.
    Used for quick context loading before the full Engine state is hydrated.
    """
    trust_level: float = Field(0.5, description="Current trust scalar (0.0-1.0)")
    resonance_profile: Dict[str, Any] = Field(default_factory=dict, description="Abstract personality weights")
    interaction_count: int = Field(0, description="Total sessions initiated")

class UserSession(BaseModel):
    """
    Complete persistent session record for a user.
    Stored in the AuthManager backend.
    """
    user_id: str = Field(..., description="Unique Subject ID from Provider (matches identity.sub)")
    identity: IdentityProfile = Field(..., description="Cached identity profile")
    tokens: TokenSet = Field(..., description="Latest token set")
    logenesis_state: LogenesisStateSummary = Field(default_factory=LogenesisStateSummary, description="Cognitive summary")
    created_at: float = Field(..., description="Session creation timestamp")
    last_accessed: float = Field(..., description="Last activity timestamp")
