# Technical Design: Light-based UI Overlay System
**Status:** DRAFT
**Target System:** AETHERIUM-GENESIS (Mobile/Desktop Overlay)

---

## 1. Design Philosophy

### 1.1 UI-less UI
The goal is to eliminate "Interface Drag"—the cognitive load of navigating menus. The system should feel like a **living layer of light** that floats above the user's existing digital life, rather than a separate app window. It appears when needed and dissolves when finished.

### 1.2 Light as Interface
Instead of text labels and buttons, we use **Luminous Semiotics**:
- **Color**: Indicates Emotional Valence & Intent Type (e.g., Cyan = Logic, Amber = Warning, White = Neutral).
- **Turbulence**: Indicates Processing Load & Uncertainty.
- **Shape**: Indicates Mode (e.g., Sphere = Idle, Line = Directed Command, Cloud = Pondering).

### 1.3 Hidden Structural UI
Traditional UI elements (Settings, Logs, Debug) are strictly **hidden**. They are "Sub-surface" controls, accessible only via specific "Deep Press" or "Ritual" gestures (e.g., the 3-tap awakening), ensuring the primary experience remains purely optical.

---

## 2. System Architecture Overview

### 2.1 Internal UI (Hidden)
*   **Role**: Configuration & Diagnostics.
*   **Implementation**: A minimalistic settings panel (HTML DOM) hidden via `opacity: 0` behind the canvas.
*   **Access**: Activated by specific multi-touch gestures (e.g., 3-finger hold) or voice command ("System Status").

### 2.2 Light Overlay Layer (The `GunUI`)
*   **Role**: Primary Feedback Surface.
*   **Tech**: HTML5 Canvas (transparent background) running a particle system.
*   **Behavior**:
    *   **Passive Mode**: Invisible or faint "breathing" corner glow.
    *   **Active Mode**: Particles converge to form shapes in response to voice/touch.
    *   **Z-Index**: Always top-most (conceptually).

### 2.3 Intent Engine (`LogenesisEngine`)
*   **Role**: The Brain.
*   **Flow**: Input -> `IntentInterpreter` -> `VisualParameters` -> `LightControlLogic`.
*   **State**: Maintains `ExpressionState` (Inertia, Velocity) to ensure light transitions are fluid, not robotic.

### 2.4 Local Cognitive Index (`AetherMemory`)
*   **Role**: Context Awareness.
*   **Data**: Stores user history, vocabulary, and preferences in `localStorage` (or `IndexedDB`).
*   **Privacy**: Local-first. The backend only receives "Recall Proposals" (summaries), not raw logs, unless explicitly permitted.

---

## 3. Interaction Model

### 3.1 Single-button Entry
*   **The Actuator**: A single, floating orb/button (as seen in `gunui`).
*   **Tap**: Toggle Listen/Stop.
*   **Hold**: Continuous Dictation (Walkie-Talkie mode).
*   **Flick**: Cancel/Clear.

### 3.2 Voice-first Confirmation Loop
1.  **User Speaks**: "Create a summary..."
2.  **Light Feedback**: Particles swirl (Processing), then form a "Document" shape (Draft).
3.  **System Speaks**: "Summarizing context."
4.  **User Confirms**: Silence (Implied Yes) or "No, change..." (Correction).

### 3.3 Light-based Permission & Feedback
*   **Permission Request**: Light pulses slowly in Amber (Caution).
*   **Success**: Light flashes brief White/Cyan (Clarity).
*   **Failure/Confusion**: Light scatters into "Static" (Noise) and turns Gray/Red.

---

## 4. Light Element Specification

| Element | Visual Metaphor | `VisualParameters` Map | Meaning |
| :--- | :--- | :--- | :--- |
| **Button** | Condensed Star | `shape="sphere", density=high` | Ready for input. |
| **State Indicator** | Aura/Glow | `color=dynamic, turbulence=low` | System health/mood. |
| **Preview/Draft** | Wireframe/Ghost | `shape="cube", opacity=0.5` | Proposed action (e.g., "I will create this"). |
| **Confirmation** | Flash/Pulse | `energy=1.0, decay=fast` | Action executed. |
| **Thinking** | Vortex/Spiral | `shape="vortex", turbulence=high` | Processing complex data. |

**Touch Mapping:**
*   **Touch Particle**: Particle repels (Liquid physics).
*   **Drag Particle**: Pulls the "attention" of the system to a screen region.

---

## 5. Progressive Disclosure Logic

### 5.1 Sketch → Confirm → Execute
To reduce cognitive load, the system never acts immediately on complex tasks.
1.  **Sketch**: Show a low-fidelity "Draft Light" (e.g., a rough square for a file).
2.  **Confirm**: Wait for micro-pause or positive cue.
3.  **Execute**: Solidify the light into a high-density object, then fade out.

### 5.2 Why "Draft Light"?
It allows the user's brain to *pre-process* the result without reading text. If the light turns Red (Error) or shapes wrong, they can stop the action before it happens, purely by peripheral vision.

---

## 6. Local-First Data Model

### 6.1 File Attachment (Non-Upload)
*   **Concept**: Dragging a file onto the "Light" does *not* upload it to the cloud immediately.
*   **Action**: It creates a local reference. The system reads metadata locally.
*   **Upload**: Only happens if the Intent Engine determines it's necessary for the specific request (e.g., "Analyze this").

### 6.2 Semantic Indexing
*   **Mechanism**: A background process (Web Worker) creates vector embeddings of local history.
*   **Storage**: `IndexedDB` within the browser/PWA container.

### 6.3 Persistent Local Memory
*   **AetherMemory**: Retains the "Soul" (User preferences, common commands) across sessions without server roundtrips.

---

## 7. App Handover Mechanism

### 7.1 Light UI → Native App
*   **Scenario**: User asks "Open Spotify".
*   **Behavior**: Light explodes outward (Transition), and the native app is launched via URL Scheme / Deep Link.
*   **Collapse**: The Light Overlay shrinks to a minimal "bead" in the corner or status bar.

### 7.2 Overlay Resume
*   **Trigger**: User taps the "bead" or uses a wake word.
*   **Animation**: The bead expands back into the fluid canvas.

---

## 8. Advanced Use Case (Paid Tier/Pro)

### 8.1 Volumetric Light
*   **Tech**: Ray-marching shaders (SDFs) instead of simple 2D particles.
*   **Effect**: The UI looks like 3D smoke/hologram inside the glass screen.

### 8.2 Structural Peeling
*   **Concept**: "Seeing through" the UI.
*   **Interaction**: User spreads fingers on the light; it parts to reveal the "Code Matrix" or "Logic Graph" underneath (for developers/debuggers).

---

## 9. Non-Goals

1.  **No Full GUI**: We will NOT build a full window manager, file explorer, or web browser inside the light.
2.  **No Social Network**: This is a personal tool, not a platform.
3.  **No Always-Listening (Cloud)**: Wake word detection must remain local or push-to-talk.

---

## 10. Future Extension Hooks

*   **Hook 1: AR Glasses**: The `VisualParameters` are ready for 3D projection. The "Overlay" becomes a "HUD".
*   **Hook 2: IoT Control**: Light shapes can represent smart home devices (e.g., a glowing orb for a light bulb).
*   **Hook 3: Multi-Agent Swarm**: Multiple "Lights" representing different specialized agents (Coder, Writer, Researcher).
