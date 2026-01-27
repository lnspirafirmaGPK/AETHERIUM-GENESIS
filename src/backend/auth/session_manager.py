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
    """
    def __init__(self, filepath: str = "auth_sessions.json"):
        self.filepath = filepath
        self._cache: Dict[str, UserSession] = {}
        self._load()

    def _load(self):
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
        try:
            data = {uid: session.model_dump(mode='json') for uid, session in self._cache.items()}
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save auth store: {e}")

    def get_user(self, user_id: str) -> Optional[UserSession]:
        return self._cache.get(user_id)

    def upsert_user(self, user_id: str, identity: IdentityProfile, tokens: TokenSet) -> UserSession:
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
