# Security Policy

## Authentication & Authorization Architecture

AETHERIUM-GENESIS employs a strictly separated identity model designed to protect cognitive state and user trust.

### 1. Identity Assurance
*   **Immutable Binding**: All user actions, memory, and intent vectors are bound to the OAuth 2.0 `sub` (Subject Identifier) provided by the Identity Provider (Google).
*   **Session Management**: Sessions are maintained via secure, signed cookies (`logenesis_session`) using `itsdangerous`.
*   **Token Handling**:
    *   **Access Tokens**: Used only server-side. Never exposed to the frontend or stored in LocalStorage.
    *   **Refresh Tokens**: Securely encrypted at rest (future phase) or stored in protected JSON (Genesis phase).

### 2. Development Exceptions (Mock Mode)
*   **Purpose**: The system supports `AUTH_PROVIDER=mock` to facilitate offline development and testing.
*   **Security Impact**:
    *   CSRF Protection is **relaxed** for the Mock provider to simplify local redirect handling.
    *   **Strict Enforcement**: In production (or when `AUTH_PROVIDER != mock`), CSRF state validation is strictly enforced. Any mismatch results in a hard 400 Bad Request.

### 3. Secret Management
*   **Environment Variables**: All sensitive credentials (Client IDs, Secrets, Signing Keys) MUST be loaded from `.env` files.
*   **Repo Hygiene**: `.env` files are gitignored. Do not commit secrets.
*   **Session Storage**: The `auth_sessions.json` file (used in Genesis phase) contains sensitive tokens and MUST be gitignored.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Genesis (Current) | :white_check_mark: |

## Reporting a Vulnerability

Please report vulnerabilities directly to the maintainers via private channels. Do not open public issues for sensitive security flaws.
