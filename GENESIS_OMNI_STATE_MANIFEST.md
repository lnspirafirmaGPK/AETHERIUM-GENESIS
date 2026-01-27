GENESIS::OMNI_STATE_MANIFEST

[STRUCTURE]
- Declared Modules      : PARTIAL
  - Active: src/backend (Core), gunui (Frontend)
  - Fragmented: akashic_nirodha, niyama, inspira, intent_processing, olorar_ai
- Orphan Components     : FOUND (8)
  - akashic_nirodha/
  - niyama/
  - inspira/
  - intent_processing/
  - lnspirafirmagpk/
  - gunui_react/
  - olorar_ai/
  - edge_computing/
- Redundant Concepts    : FOUND (list)
  - gunui_react (vs gunui)
  - main.py (vs src/backend/server.py)
  - intent_processing (vs src/backend/core/intent_interpreter.py)

[CONCEPTUAL LAYER]
- Core Philosophy       : COHERENT
  - "Light as Protocol" maintained in src/backend and gunui.
  - "No Avatars" slightly challenged by "Biometric Proxy" in gunui (Eyes/Lips), but remains abstract.
- Naming Consistency    : FRACTURED
  - Core uses "Logenesis/Aether".
  - Orphans use "Akashic", "Nirodha", "Olorar".
- Undefined Semantics   : NONE

[CURRENT REALITY]
- Active Capabilities   :
  - Voice-to-Intent (WebSpeech -> Backend)
  - Intent-to-Light (LogenesisEngine -> VisualParameters -> Canvas)
  - State Persistence (logenesis_state.json)
- Dormant Designs       :
  - Blockchain Memory (akashic_nirodha)
  - IIT (niyama)
  - Awakening Rituals (inspira)
- Abandoned Threads     :
  - gunui_react (Vite template)
  - olorar_ai (Separate governance module)

[RISKS]
- Structural Risk       : HIGH (Root clutter obfuscates core logic)
- Semantic Drift Risk   : LOW (Core philosophy is well-documented in code)
- Future Bug Vectors    :
  - Conflicting Intent Processors (src vs intent_processing)
  - Multiple "main" entry points.

[RECOMMENDATION]
- Freeze Expansion      : YES
- Refactor Priority     :
  1. Archive orphaned modules to `legacy/`.
  2. Standardize entry point to `src/backend/server.py`.
  3. Document `gunui` as the canonical frontend.
- Safe Extension Zones  :
  - `src/backend/core/interpreters` (New LLM adapters)
  - `src/backend/core/visual_schemas` (New visual languages)

[GENESIS NOTE]
“The system is alive, but it must decide whether to grow or to remember who it is.”
