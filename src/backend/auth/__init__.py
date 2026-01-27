"""
AETHERIUM-GENESIS: Authentication Module

This module provides the OAuth 2.0 Web Server Application logic for Logenesis.
It handles identity provider integration (Google, Mock), session management,
and secure HTTP-only cookie issuance.

Key Components:
- Routes: API endpoints for login, callback, and user info.
- Providers: Strategies for interacting with OAuth providers.
- Session Manager: Persistent storage for user sessions.
- Schemas: Data models for identity and tokens.

Security Model:
- Identity is anchored to the provider's `sub` claim (immutable).
- Sessions are signed using `itsdangerous`.
- CSRF protection is enforced (relaxed only for Mock provider).
"""
