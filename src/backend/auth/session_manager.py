import json
import os
import time
import logging
from typing import Optional, Dict
from .schemas import UserSession, TokenSet, IdentityProfile

logger = logging.getLogger("AuthManager")

class AuthManager:
    """
    Manages persistent user identities and sessions using a JSON store.

    This implementation is designed for the 'Genesis Phase' (single-node, low-scale).
    It loads the entire session database into memory on startup and persists to a JSON file.

    Attributes:
        filepath (str): Path to the JSON storage file (default: auth_sessions.json).
        _cache (Dict[str, UserSession]): In-memory cache of active sessions keyed by user_id.
    """
    def __init__(self, filepath: str = "auth_sessions.json"):
        self.filepath = filepath
        self._cache: Dict[str, UserSession] = {}
        self._load()

    def _load(self):
        """Loads sessions from the JSON file into the memory cache."""
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                for uid, user_data in data.items():
                    self._cache[uid] = UserSession(**user_data)
            logger.info(f"Loaded {len(self._cache)} identities from store.")
        except Exception as e:
            logger.error(f"Failed to load auth store: {e}")

    def save(self):
        """Persists the current in-memory cache to the JSON file."""
        try:
            data = {uid: session.model_dump(mode='json') for uid, session in self._cache.items()}
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save auth store: {e}")

    def get_user(self, user_id: str) -> Optional[UserSession]:
        """
        Retrieves a session by User ID.

        Args:
            user_id (str): The unique Subject ID (sub).

        Returns:
            Optional[UserSession]: The session object if found, else None.
        """
        return self._cache.get(user_id)

    def upsert_user(self, user_id: str, identity: IdentityProfile, tokens: TokenSet) -> UserSession:
        """
        Creates or updates a user session.

        - If user exists: Updates profile, tokens, and last_accessed time.
        - If new: Creates a new session record.

        Args:
            user_id (str): The unique Subject ID (sub).
            identity (IdentityProfile): The latest profile from the provider.
            tokens (TokenSet): The new access/refresh tokens.

        Returns:
            UserSession: The updated session object.
        """
        now = time.time()

        if user_id in self._cache:
            # Update existing
            session = self._cache[user_id]
            session.identity = identity # Update profile if changed
            session.tokens = tokens     # Rotate tokens
            session.last_accessed = now
        else:
            # Create new
            session = UserSession(
                user_id=user_id,
                identity=identity,
                tokens=tokens,
                created_at=now,
                last_accessed=now
            )
            self._cache[user_id] = session

        self.save()
        return session
