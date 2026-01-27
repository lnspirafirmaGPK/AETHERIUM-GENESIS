# Logenesis / AETHERIUM-GENESIS: OAuth 2.0 Identity Architecture

## 1. Core Principle: Identity as Continuity
In Logenesis, "Identity" is not merely a login credential but the **Cognitive Anchor**. It binds the system's memory, resonance (personality state), and intent vectors to a continuous thread of existence.

### 1.1 The Role of OAuth 2.0
We utilize the **Authorization Code Flow** for Web Server Applications. This is chosen specifically because:
1.  **Server-Side Security**: Client Secrets are never exposed to the frontend (GunUI).
2.  **Long-Lived Access**: Refresh tokens allow the backend (Cognitive Core) to maintain state even when the UI is closed.
3.  **Trust Model**: By leveraging Google (or similar Enterprise-grade IdPs), we inherit a robust trust infrastructure rather than reinventing weak authentication.

## 2. Architecture Components

### 2.1 Backend (Reasoning Core)
*   **Module**: `src.backend.auth`
*   **Responsibility**:
    *   Initiate OAuth redirects.
    *   Exchange Authorization Codes for Tokens (Access + Refresh).
    *   Create and sign secure HTTP-only sessions.
    *   **Crucially**: Map external identity to internal cognitive state.
*   **Storage**:
    *   **Genesis Phase**: JSON-based file storage (`auth_sessions.json`).
    *   **Future Phase**: Distributed Key-Value Store (Redis/Postgres).

### 2.2 Frontend (GunUI / Visual Cortex)
*   **Role**: Purely presentational.
*   **Interaction**:
    *   A single "Connect Identity" button triggers the flow.
    *   The UI **never** sees tokens. It only receives a session cookie (HTTP-only) which browsers handle automatically.
    *   The UI polls `/auth/me` to determine if it should render the "Identity Linked" state.

## 3. Key Design Decisions

### 3.1 Immutable Identity (`sub` vs `email`)
**Decision**: We strictly use the OpenID Connect `sub` (Subject Identifier) as the primary user ID.
**Reasoning**:
*   **`email` is mutable**: Users can change emails, or recycle them. Relying on email breaks the continuity of the cognitive graph.
*   **`sub` is immutable**: The IdP guarantees this ID never changes for the same account.
*   **Impact**: Memory nodes and Trust scores are keyed to `sub`. Email is treated merely as a display attribute.

### 3.2 Security Posture
*   **CSRF Protection**: State parameters are strictly enforced for production providers. (Exception: Mock provider for local dev).
*   **Session Cookies**: Signed using `itsdangerous`, `HttpOnly`, `SameSite=Lax`.
*   **Secret Management**: All credentials loaded via `.env` (never committed).

## 4. Environment Strategy
*   **Production**: `AUTH_PROVIDER=google`. Requires valid Client ID/Secret.
*   **Development**: `AUTH_PROVIDER=mock`. Uses a simulated flow that bypasses external calls but maintains the exact same architectural contract (redirect -> callback -> session).

## 5. Future Scalability
This architecture is designed to support:
*   **Multi-Modal Identity**: Binding voice biometrics to the same `sub`.
*   **Federated Learning**: Using the `sub` to key personalized model fine-tuning.
*   **Edge Auth**: Propagating the signed session to edge nodes via secure mesh protocols.
