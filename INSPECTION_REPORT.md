# System Inspection Report – AETHERIUM-GENESIS

## Core Execution Flow
*   **Intent Engine**:
    *   `src/backend/core/logenesis_engine.py`: The `LogenesisEngine` class acts as the central Intent Engine. It orchestrates the transition between 'Nirodha' and 'Awakened' states and manages the interpretation pipeline.
*   **Execution Flow (Input → Interpretation → Output)**:
    1.  **Input**:
        *   `src/backend/server.py`: WebSocket endpoint (`/ws`) receives `INTENT_RECOGNIZED` (text) or legacy `logenesis` JSON payloads.
    2.  **Interpretation**:
        *   `LogenesisEngine.process()` calls `self.interpreter.interpret(text)`.
        *   Interpreter (`src/backend/core/gemini_interpreter.py` or `simulated_interpreter.py`) converts Natural Language → `VisualParameters` (JSON).
    3.  **State Evolution**:
        *   `LogenesisEngine._drift_state()` maps `VisualParameters` to `IntentVector` to calculate "Drift" (Inertia/Velocity) and updates `logenesis_state.json`.
    4.  **Output**:
        *   `LogenesisEngine` returns `LogenesisResponse`.
        *   `server.py` transforms this into Client Protocol messages: `VISUAL_PARAMS` (for particle morphing), `AI_SPEAK` (for TTS), or raw state updates.

## UI / Visualization Layer
*   **Visualization Logic**:
    *   **Primary (Living Interface)**: `index.html` (Root). Contains `GunUI` class and `Particle` class using HTML5 Canvas (`#gun-canvas`). Logic includes `nirodha` (sleep) physics vs `manifestation` (target-seeking) physics.
    *   **Secondary (Actuator UI)**: `gunui/index.html`. A separate implementation focusing on Voice Interaction (`webkitSpeechRecognition`) with its own particle system (Hue shifting, Pulse).
    *   **Backend Support**: `src/backend/core/formation_manager.py` calculates coordinate sets for specific shapes (Circle, Square, etc.) to be sent to the frontend.
*   **Real UI vs. Debug/Placeholder**:
    *   **Real UI**: The Particle System (`#gun-canvas`) and the "Ritual Layer" (Tap 3 times) in `index.html`.
    *   **Overlay UI**: `#ui-layer` in `index.html` serves as the "Heads-Up Display" (Status Glow, PHI RES, Terminal Logs).
    *   **Debug/Legacy**: `visual_engine.py` and `main.py` appear to be legacy local runners, as the architecture has shifted to `server.py` + Web Frontend.

## State & Memory
*   **Local-first Memory**:
    *   **Frontend**: `index.html` uses `AetherMemory` class which persists to `localStorage` key `aetherium_core_memory`. Stores `awakening_count`, `last_awakened_at`, and `conversations`.
    *   **Backend**: `src/backend/core/logenesis_engine.py` uses `StateStore` to save/load `ExpressionState` (Inertia, Vector) to `logenesis_state.json`.
*   **Long-lived vs. Transient**:
    *   **Long-lived**: `genesis_core.json` (Core Memories/Soul), `logenesis_state.json` (Drift State), `localStorage` (User interaction history).
    *   **Transient**: Real-time particle positions, WebSocket connection state, current `VisualParameters`.

## Things That Conflict With Light-based Overlay Philosophy
*   **Traditional UI Elements**:
    *   `#recall-modal` in `index.html`: Uses a standard HTML modal with "IGNORE" and "RECALL" buttons. This breaks the immersion of the "Living Interface".
    *   `#input-layer` in `index.html`: A standard HTML `<input>` text box. While hidden by default (toggled via Ctrl+Enter), it is a mechanical artifact.
    *   `gunui/index.html`: The "Touch to speak" button (`.actuator`) is a stylized but traditional clickable button.
*   **Menu Assumptions**:
    *   The `recall-modal` explicitly requires a user to "Click" a button to confirm memory integration.
    *   The `GunUI` in `index.html` relies on keyboard shortcuts (`Ctrl+Enter`) for text input, assuming a desktop environment rather than a fluid, ambient interface.

## Keep / Refactor / Remove
*   **Keep (Core)**:
    *   `src/backend/core/logenesis_engine.py`: The brain.
    *   `src/backend/server.py`: The nervous system.
    *   `index.html` (Root): The primary body/vessel.
*   **Refactor (Sub-surface)**:
    *   `#recall-modal` in `index.html`: Should be replaced with a gesture (e.g., "Tap and hold to absorb memory") or a light-based signal (e.g., "Catch the glowing orb").
    *   `#input-layer`: Could be replaced or augmented with the Voice Interaction logic from `gunui/index.html` to remove reliance on the keyboard.
*   **Remove / Archive**:
    *   `visual_engine.py` & `main.py`: Seem redundant given the `server.py` architecture.
    *   `gunui/index.html`: Its voice capabilities (STT/VAD) should be merged into the root `index.html`, and this file removed to avoid split-brain UI logic.
