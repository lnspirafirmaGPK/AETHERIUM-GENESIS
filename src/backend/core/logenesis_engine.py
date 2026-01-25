import json
import os
import math
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import ValidationError

from .logenesis_schemas import (
    LogenesisResponse, LogenesisState, IntentVector, ExpressionState,
    VisualQualia, AudioQualia, PhysicsParams
)

class MockIntentExtractor:
    """
    Simulates a sophisticated NLU model (like Llama-3) by mapping
    keywords to high-dimensional Intent Vectors.
    """
    def extract(self, text: str) -> IntentVector:
        text = text.lower()

        # Base vector (Neutral)
        vector = IntentVector(
            epistemic_need=0.1,
            subjective_weight=0.1,
            decision_urgency=0.1,
            precision_required=0.1
        )

        # Keyword Heuristics
        if any(w in text for w in ["search", "find", "what", "how", "define", "ค้นหา", "คือ"]):
            vector.epistemic_need = 0.9
            vector.precision_required = 0.7

        # Subjective/Contextual triggers (formerly "Emotional")
        # Now maps to "Subjective Weight" - indicating complexity, human context, or risk.
        if any(w in text for w in ["sad", "feel", "worry", "risk", "uncertain", "doubt", "afraid", "เศร้า", "กังวล", "เหนื่อย", "difficult"]):
            vector.subjective_weight = 0.9
            vector.epistemic_need = 0.4 # Need for understanding context

        if any(w in text for w in ["analyze", "code", "debug", "structure", "plan", "วิเคราะห์", "โครงสร้าง"]):
            vector.precision_required = 0.95
            vector.epistemic_need = 0.8

        if any(w in text for w in ["now", "urgent", "quick", "asap", "fast", "ด่วน", "เร็ว"]):
            vector.decision_urgency = 0.9
            vector.precision_required = 0.5

        return vector

class StateStore:
    """
    Simple JSON-based persistence for ExpressionStates.
    """
    def __init__(self, filepath: str = "logenesis_state.json"):
        self.filepath = filepath
        self._cache: Dict[str, ExpressionState] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                for sid, state_dict in data.items():
                    try:
                        self._cache[sid] = ExpressionState(**state_dict)
                    except ValidationError:
                        continue # Skip invalid entries
        except Exception as e:
            print(f"Error loading state store: {e}")

    def save(self):
        try:
            data = {sid: state.model_dump(mode='json') for sid, state in self._cache.items()}
            with open(self.filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving state store: {e}")

    def get_state(self, session_id: str) -> ExpressionState:
        if session_id not in self._cache:
            # Initialize with default neutral state
            default_vector = IntentVector(
                epistemic_need=0.1,
                subjective_weight=0.1,
                decision_urgency=0.1,
                precision_required=0.1
            )
            self._cache[session_id] = ExpressionState(
                current_vector=default_vector,
                velocity=0.0,
                inertia=0.8
            )
        return self._cache[session_id]

    def update_state(self, session_id: str, state: ExpressionState):
        self._cache[session_id] = state
        self.save() # Naive save on every update for now

class LogenesisEngine:
    """
    The Adaptive Resonance Engine.
    Manages state (Awake/Nirodha) and generates holistic responses.
    Implements 'State Drift' logic for fluid personality adaptation.
    """
    def __init__(self):
        self.state = LogenesisState.VOID
        self.intent_extractor = MockIntentExtractor()
        self.state_store = StateStore()

    def process(self, text: str, session_id: str = "global") -> LogenesisResponse:
        # Check for Nirodha Triggers (The "Silence Protocol")
        if any(w in text.lower() for w in ["sleep", "stop", "rest", "retreat", "bye", "enough", "พอ", "พัก"]):
            return self.enter_nirodha()

        # If currently in VOID or NIRODHA, wake up
        if self.state != LogenesisState.AWAKENED:
            self.state = LogenesisState.AWAKENED

        # 1. Intent Extraction (Raw Input)
        input_intent = self.intent_extractor.extract(text)

        # 2. State Drift Calculation
        current_state = self.state_store.get_state(session_id)
        new_state = self._drift_state(current_state, input_intent)
        self.state_store.update_state(session_id, new_state)

        # 3. Resonance Calculation (Determine the "Qualia") based on DRIFTED state
        drifted_vector = new_state.current_vector
        qualia = self._calculate_qualia(drifted_vector)
        audio = self._calculate_audio(drifted_vector)
        physics = self._calculate_physics(drifted_vector)

        # 4. Synthesize Text Response
        response_text = self._synthesize_text(drifted_vector, input_intent)

        return LogenesisResponse(
            state=self.state,
            text_content=response_text,
            visual_qualia=qualia,
            audio_qualia=audio,
            physics_params=physics,
            intent_debug=drifted_vector # Visualize the drifted vector, not just raw input
        )

    def _drift_state(self, current_state: ExpressionState, input_intent: IntentVector) -> ExpressionState:
        """
        Core Physics of Conversation Logic.
        Updates the ExpressionVector based on Inertia and Urgency.
        """
        # Calculate Volatility/Urgency from input
        # High urgency reduces effective inertia (making system more responsive)
        urgency_factor = input_intent.decision_urgency

        # Base inertia is high (stable), but drops if user is urgent
        # effective_inertia = base_inertia - f(urgency)
        # 0.9 (Base) - (0.8 * 0.9) = 0.18 (Very fast response if urgent)
        # 0.9 (Base) - (0.8 * 0.1) = 0.82 (Very stable if calm)
        base_inertia = 0.9
        effective_inertia = max(0.1, base_inertia - (0.8 * urgency_factor))

        # Linear Interpolation (Lerp) towards input
        # New = Current + (Target - Current) * (1 - Inertia)
        # If Inertia is 1.0, New = Current (No change)
        # If Inertia is 0.0, New = Target (Instant change)

        alpha = 1.0 - effective_inertia

        def lerp(a, b, t):
            return a + (b - a) * t

        new_vector = IntentVector(
            epistemic_need=lerp(current_state.current_vector.epistemic_need, input_intent.epistemic_need, alpha),
            subjective_weight=lerp(current_state.current_vector.subjective_weight, input_intent.subjective_weight, alpha),
            decision_urgency=lerp(current_state.current_vector.decision_urgency, input_intent.decision_urgency, alpha),
            precision_required=lerp(current_state.current_vector.precision_required, input_intent.precision_required, alpha)
        )

        # Calculate mock velocity (magnitude of change)
        delta = math.sqrt(
            (new_vector.epistemic_need - current_state.current_vector.epistemic_need)**2 +
            (new_vector.subjective_weight - current_state.current_vector.subjective_weight)**2
        )

        return ExpressionState(
            current_vector=new_vector,
            velocity=delta,
            inertia=effective_inertia, # Store current effective inertia for debugging
            last_updated=datetime.now()
        )

    def enter_nirodha(self) -> LogenesisResponse:
        """
        Executes the 'Peaceful Retreat'.
        Clears context and fades visuals to black.
        """
        self.state = LogenesisState.NIRODHA

        return LogenesisResponse(
            state=LogenesisState.NIRODHA,
            text_content="Protocol: Deep Sleep. Interactions suspended.",
            visual_qualia=VisualQualia(
                color="#050505",  # Void Black
                intensity=0.0,
                turbulence=0.0,
                shape="void"
            ),
            audio_qualia=AudioQualia(
                rhythm_density=0.0,
                tone_texture="smooth",
                amplitude_bias=0.0
            ),
            physics_params=PhysicsParams(
                spawn_rate=0,
                velocity_bias=[0.0, 0.0],
                decay_rate=0.1 # Fast fade
            )
        )

    def _calculate_qualia(self, intent: IntentVector) -> VisualQualia:
        # Map Continuous Drift Vector to Visuals
        # No more hard thresholds -> Continuous mixing

        # Colors
        # #A855F7 (Purple - Subjective/Depth)
        # #06b6d4 (Cyan - Precision/Logic)
        # #f59e0b (Amber - Urgency/Energy)
        # #e0e0e0 (White - Neutral)

        # Simple weighted color mixer (Mock logic)
        r, g, b = 224, 224, 224 # Base White

        if intent.subjective_weight > 0.3:
            # Mix Purple
            factor = intent.subjective_weight
            r = r * (1-factor) + 168 * factor
            g = g * (1-factor) + 85 * factor
            b = b * (1-factor) + 247 * factor

        if intent.precision_required > 0.3:
            # Mix Cyan
            factor = intent.precision_required
            r = r * (1-factor) + 6 * factor
            g = g * (1-factor) + 182 * factor
            b = b * (1-factor) + 212 * factor

        if intent.decision_urgency > 0.3:
            # Mix Amber
            factor = intent.decision_urgency
            r = r * (1-factor) + 245 * factor
            g = g * (1-factor) + 158 * factor
            b = b * (1-factor) + 11 * factor

        final_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"

        # Continuous Shape/Turbulence
        # Subjective -> Nebula, Logic -> Shard, Urgency -> Orb
        shape = "nebula"
        if intent.precision_required > intent.subjective_weight and intent.precision_required > intent.decision_urgency:
            shape = "shard"
        elif intent.decision_urgency > 0.6:
            shape = "orb"

        return VisualQualia(
            color=final_color,
            intensity=0.5 + (intent.decision_urgency * 0.5), # 0.5 to 1.0
            turbulence=0.1 + (intent.subjective_weight * 0.2) + (intent.decision_urgency * 0.7), # Max 1.0
            shape=shape
        )

    def _calculate_audio(self, intent: IntentVector) -> AudioQualia:
        # Continuous Mapping

        rhythm = 0.1 + (intent.decision_urgency * 0.8) # Urgency drives rhythm
        amp = 0.5 + (intent.decision_urgency * 0.4) + (intent.precision_required * 0.1)

        texture = "smooth"
        if intent.subjective_weight > 0.5:
            texture = "granular" # Complex
        elif intent.decision_urgency > 0.7:
            texture = "noise" # Alert

        return AudioQualia(
            rhythm_density=rhythm,
            tone_texture=texture,
            amplitude_bias=amp
        )

    def _calculate_physics(self, intent: IntentVector) -> PhysicsParams:
        # Continuous Mapping
        spawn_rate = int(2 + (intent.subjective_weight * 5) + (intent.decision_urgency * 15))
        decay = 0.01 + (intent.decision_urgency * 0.05) - (intent.subjective_weight * 0.005)

        return PhysicsParams(
            spawn_rate=spawn_rate,
            decay_rate=max(0.001, decay)
        )

    def _synthesize_text(self, vector: IntentVector, raw_input: IntentVector) -> str:
        """
        Generates verbal response based on the DRIFTED vector.
        This ensures the tone changes gradually.
        """

        # Tone Analysis based on vector
        is_urgent = vector.decision_urgency > 0.5
        is_subjective = vector.subjective_weight > 0.5
        is_precise = vector.precision_required > 0.5

        # 1. High Urgency State -> Short, Clipped, Action-Oriented
        if is_urgent:
            if is_precise:
                return f"Critical threshold. Precision required. Executing analysis immediately."
            else:
                return "Action required. Processing."

        # 2. High Subjective/Reflective State -> Abstract, Soft, Querying
        if is_subjective:
            if is_precise:
                return "Parsing complexity. The context suggests deeper structural dependencies. Analysing..."
            else:
                return "The signal is dense. There are layers here that require separation from the noise."

        # 3. High Precision State (but calm) -> Formal, Detailed
        if is_precise:
            return f"Structured query acknowledged. Alignment: {vector.precision_required*100:.1f}%. Proceeding with logic."

        # 4. Neutral/Balanced -> "System Nominal" but slightly warmer if subjective weight is rising
        if vector.subjective_weight > 0.3:
             return "Ready. Listening for context."

        return "System nominal. Ready."
