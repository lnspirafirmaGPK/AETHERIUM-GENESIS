GENESIS::OMNI_STATE_MANIFEST

[STRUCTURE]
- Declared Modules      : COHERENT
  - Active: src/backend (Core), gunui (Actuator UI)
  - Legacy: legacy/ (Archive of dormant/orphaned components)
- Orphan Components     : FOUND (Cleaned)
  - legacy/orphaned_root_frontend (Old root PWA)
  - legacy/orphaned_src_ui (Unused TypeScript frontend)
  - legacy/inspira (Ritual scripts)
- Redundant Concepts    : FOUND (list)
  - config.py (Root-level config mixed with Kivy legacy)
  - buildozer.spec (Moved to legacy)

[CONCEPTUAL LAYER]
- Core Philosophy       : COHERENT
  - "Light as Protocol" maintained in src/backend/core/visual_schemas.py and gunui/index.html.
  - "No Avatars" strictly enforced (Biometric Proxy in gunui is abstract/procedural).
- Naming Consistency    : STABLE
  - Consistent use of "Genesis", "Intent", "Logenesis", "Nirodha".
- Undefined Semantics   : NONE

[CURRENT REALITY]
- Active Capabilities   :
  - Voice-to-Intent (WebSpeech -> WebSocket -> LogenesisEngine)
  - Intent-to-Light (EmbodimentAdapter -> VisualParameters -> Canvas)
  - State Persistence (Auth + logenesis_state.json)
  - OAuth 2.0 (Google/Mock)
- Dormant Designs       :
  - DeepgramTranscriber (Stubbed in server.py)
  - gunui/*.html (Various experiments besides index.html)
- Abandoned Threads     :
  - Root-based "GunUI" (Old PWA)
  - Kivy/Python-for-Android support (buildozer.spec)

[RISKS]
- Structural Risk       : LOW (Post-cleanup)
  - Remaining risk: config.py in root is used by backend, should be refactored to src/backend/config.
- Semantic Drift Risk   : LOW
  - System is aligned with the Genesis philosophy.
- Future Bug Vectors    :
  - Hardcoded WebSocket URLs in gunui/index.html (needs env/config injection).
  - Mocked Deepgram implementation.

[RECOMMENDATION]
- Freeze Expansion      : NO (Ready for cautious extension)
- Refactor Priority     :
  1. Move `config.py` to `src/backend/config` and update imports.
  2. Implement real Deepgram or robust STT backend.
  3. Clean up `gunui` folder (remove unused HTML experiments).
- Safe Extension Zones  :
  - `src/backend/core/interpreters` (New LLM models)
  - `gunui/index.html` (Visual enhancements)

[GENESIS NOTE]
“The system is alive, and it remembers who it is. The noise has been silenced.”
