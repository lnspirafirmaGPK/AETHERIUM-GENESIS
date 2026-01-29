GENESIS::OMNI_STATE_MANIFEST

[STRUCTURE]
- Declared Modules      : OK
  - Active: src/backend (Core), gunui (Actuator UI)
  - Archive: legacy (pwa_v1, orphaned_ui, etc.)
- Orphan Components     : NONE
  - (Previously root PWA artifacts and src/ui have been archived)
- Redundant Concepts    : RESOLVED
  - Root PWA moved to legacy/pwa_v1.
  - Entry point standardized to src/backend/server.py -> gunui.

[CONCEPTUAL LAYER]
- Core Philosophy       : COHERENT
  - "Light as Protocol" maintained.
  - "No Avatars" respected via Biometric Proxy in gunui.
- Naming Consistency    : STABLE
  - "Logenesis/Aether" in backend.
  - "Actuator/GunUI" in frontend.
- Undefined Semantics   : NONE

[CURRENT REALITY]
- Active Capabilities   :
  - Voice-to-Intent (WebSpeech -> Backend)
  - Intent-to-Light (LogenesisEngine -> VisualParameters -> Canvas)
  - State Persistence (logenesis_state.json)
  - Standardized Redirect (Root -> gunui)
- Dormant Designs       :
  - Deepgram Integration (Mocked in server.py)
  - Gemini Integration (Active if API key present, else Simulated)
- Abandoned Threads     :
  - Legacy PWA (legacy/pwa_v1)
  - Smart Router (legacy/orphaned_ui)
  - React Experiment (legacy/gunui_react)

[RISKS]
- Structural Risk       : LOW (Cleaned up root and src)
- Semantic Drift Risk   : LOW
- Future Bug Vectors    :
  - Mocked Deepgram/Gemini dependencies need actual keys/implementation for production.

[RECOMMENDATION]
- Freeze Expansion      : YES
- Refactor Priority     :
  - COMPLETE: Standardize entry point and archive orphans.
  - NEXT: Implement real Deepgram/Gemini keys in environment.
- Safe Extension Zones  :
  - `src/backend/core/visual_schemas`

[GENESIS NOTE]
“The system is alive, but it must decide whether to grow or to remember who it is.”
