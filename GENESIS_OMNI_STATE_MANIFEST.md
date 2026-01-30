GENESIS::OMNI_STATE_MANIFEST

[STRUCTURE]
- Declared Modules      : OK
  - Active: src/backend (Core), gunui (Frontend)
  - Hybrid: config.py (Auth/Legacy Settings)
- Orphan Components     : NONE (All archived in legacy/)
- Redundant Concepts    : FOUND (list)
  - legacy/orphaned_ui (vs gunui)
  - legacy/pwa_v1 (vs gunui)
  - legacy/kivy_specs (vs Web Platform)

[CONCEPTUAL LAYER]
- Core Philosophy       : COHERENT
  - "Light as Protocol" strictly enforced in gunui.
  - "No Avatars" adherence is high (Biometric Proxy is abstract).
- Naming Consistency    : IMPROVING
  - Core uses "Logenesis/Aether".
  - Legacy concepts quarantined.
- Undefined Semantics   : NONE

[CURRENT REALITY]
- Active Capabilities   :
  - Voice-to-Intent (WebSpeech -> Backend)
  - Intent-to-Light (LogenesisEngine -> VisualParameters -> Canvas)
  - State Persistence (Session-based)
- Dormant Designs       :
  - Blockchain Memory (legacy/akashic_nirodha)
  - IIT (legacy/niyama)
  - Awakening Rituals (legacy/inspira)
  - Kivy Mobile App (legacy/kivy_specs)
- Abandoned Threads     :
  - gunui_react (legacy/gunui_react)
  - TypeScript Frontend (legacy/orphaned_ui)
  - Root PWA (legacy/pwa_v1)

[RISKS]
- Structural Risk       : LOW (Root is clean, separation is clear)
- Semantic Drift Risk   : MEDIUM (config.py mixes Auth with Legacy Rituals)
- Future Bug Vectors    :
  - Dependency on legacy keys in config.py for new features.

[RECOMMENDATION]
- Freeze Expansion      : YES
- Refactor Priority     :
  1. Refactor `config.py` to separate Auth from Legacy.
  2. Ensure `src/backend` remains the sole source of truth for logic.
- Safe Extension Zones  :
  - `src/backend/core/interpreters`
  - `src/backend/core/visual_schemas`

[GENESIS NOTE]
“The system is alive, but it must decide whether to grow or to remember who it is.”
