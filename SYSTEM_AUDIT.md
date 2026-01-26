# System Internal Audit for AETHERIUM-GENESIS
**Status:** Current State Report
**Date:** 2024-05-22
**Auditor:** Juice (AI Agent)

---

## 1. Repository Topology

**Structure:**
The repository is a hybrid of a structured Python backend and multiple experimental/legacy folders.

*   **`src/backend/core`**: The true "Core". Contains `LogenesisEngine`, `IntentInterpreter`, and Pydantic schemas. This is where the reasoning logic lives.
*   **`src/backend/server.py`**: The entry point for the FastAPI/WebSocket server.
*   **`gunui/`**: The active frontend development folder. Contains the "Actuator UI" (`gunui/index.html`).
*   **`index.html`**: The legacy "Living Interface" PWA at the root.
*   **`main.py` & `visual_engine.py`**: A standalone simulation runner that opens HTML files in a browser and mimics the "Ritual" in the console. Not integrated with the FastAPI server directly.
*   **Experimental/Legacy Modules**:
    *   `akashic_nirodha/`: Blockchain/Storage experiments (Unused).
    *   `niyama/`: Integrated Information Theory experiments (Unused).
    *   `inspira/`: Awakening ritual scripts (Unused).
    *   `intent_processing/`: Standalone intent logic (Unused by `src/backend`).

**Coupling:**
*   **High Coupling**: `LogenesisEngine` is tightly coupled to `IntentInterpreter` subclasses (Gemini/Simulated) and `FormationManager`.
*   **Low Coupling**: The Frontend (`gunui`) and Backend (`src`) are decoupled via WebSocket, sharing only JSON contracts (`VISUAL_PARAMS`).

---

## 2. UI / Interaction Layer

**UI Types:**

| UI Name | Type | Status | Description |
| :--- | :--- | :--- | :--- |
| **Actuator UI** (`gunui/index.html`) | Direct UI | **Active** | The new voice-first interface. Renders particles based on `VISUAL_PARAMS`. |
| **Living Interface** (`index.html`) | Direct UI | Legacy | The original PWA with "Nirodha" and "Manifestation" states. Uses `AetherMemory`. |
| **Console Simulation** (`main.py`) | Simulation Tool | Secondary | CLI-based interaction that launches browser windows. Useful for demos, not production. |
| **Visual Engine** (`visual_engine.py`) | Helper | Secondary | Python wrapper to launch the HTML files. |

**User Facing:**
*   `gunui/index.html` (The intended future interface).
*   `index.html` (The previous "Vessel" concept).

**Internal Only:**
*   `nirodha_standby.html` (Placeholder standby screen).
*   `generative_ui.html` (Experimental).

---

## 3. Intent → Action Pipeline

**Flow:**
1.  **Input**: User speaks (Voice) or types (Text) -> Frontend captures -> Sends `INTENT_RECOGNIZED` (WS).
2.  **Processing** (`LogenesisEngine.process`):
    *   **Nirodha Check**: Checks for hardcoded keywords ("sleep", "stop") -> Enters void state.
    *   **Interpretation**: `IntentInterpreter` (Gemini or Simulated) converts text -> `VisualParameters` (JSON).
    *   **Mapping**: `VisualParameters` are mapped to legacy `IntentVector` (Subjective, Epistemic, Urgency) via hardcoded rules in `_map_visual_to_intent_vector`.
    *   **Drift Calculation**: Current state drifts towards new vector based on Physics (Inertia, Velocity).
3.  **Output**: `LogenesisResponse` containing:
    *   `VisualParameters` (for Frontend rendering).
    *   `TextContent` (Synthesized system response, e.g., "Core stability maintained").
4.  **Action**: Frontend receives JSON -> Adjusts particle `turbulence`, `color`, `target` shapes.

**Hard-coded Logic:**
*   **Keyword Triggers**: "sleep", "stop" etc. in `process()`.
*   **Intent Mapping**: Rules mapping `IntentCategory` (Chat, Command) to specific numeric vector values.
*   **Response Templates**: "Critical variance detected", "Signal weight acknowledged" are hardcoded strings.

---

## 4. Visualization / Rendering Logic

**Rendering Layers:**
*   **Backend (Logic)**: `FormationManager` calculates target coordinates for specific shapes (Circle, Line). `LogenesisEngine` calculates "Qualia" (Color, Turbulence).
*   **Frontend (Rasterization)**: HTML5 Canvas.
    *   `gunui`: Uses `requestAnimationFrame` loop. Maps `VISUAL_PARAMS` to particle physics (velocity, damping). Contains its own shape generation logic (`generateShapeTargets`) which **duplicates** backend logic.
    *   `index.html`: Has `FaceTopology` class for face mapping.

**Assumptions:**
*   **Screenless-ish**: The design assumes a full-screen canvas with no standard widgets (buttons, nav bars).
*   **Resolution**: Backend `FormationManager` assumes 1920x1080 default for coordinate calculation.

---

## 5. Data Handling Model

**Storage:**
*   **Backend**: `logenesis_state.json` (Local File). Stores session state (Inertia, Vector).
*   **Frontend**: `localStorage` (`AetherMemory`). Stores conversation history and "Awakening Count".

**Local vs Remote:**
*   **Hybrid**: Intent interpretation uses `google.generativeai` (Remote LLM) if API key exists. Fallback is local regex/keyword.
*   **Privacy**: Backend does not store conversation logs permanently (only transient session state). Frontend stores logs.

**Issues:**
*   **Duplication**: `AetherMemory` logic in `index.html` is robust but not fully utilized by `gunui`.
*   **Redundant Exports**: `LogenesisResponse` sends full `IntentVector` debug data which the `gunui` frontend largely ignores (it cares about `VisualParameters`).

---

## 6. Feature Inventory

| Feature Name | Status | Dependency | Risk if Removed |
| :--- | :--- | :--- | :--- |
| **Logenesis Engine** | **Core** | `pydantic`, `numpy` | **Critical**. The brain of the system. |
| **Gemini Interpreter** | **Core** | `google-generativeai` | High. Loss of natural language understanding. |
| **Simulated Interpreter** | Fallback | None | Low. Only needed if offline. |
| **Formation Manager** | **Core** | `numpy` | Medium. Defines shape geometry. |
| **GunUI (Actuator)** | **Core** | Browser Speech API | **Critical**. The current UI. |
| **Legacy PWA (`index.html`)** | Legacy | Browser | Low. Can be archived. |
| **Visual Engine (`main.py`)** | Utility | None | Low. Just a demo runner. |
| **Akashic Nirodha** | Unused | None | None. Dead code. |
| **Niyama (IIT)** | Unused | None | None. Dead code. |
| **Inspira Ritual** | Unused | None | None. Dead code. |
| **Intent Processing** | Unused | None | None. Duplicate logic. |
