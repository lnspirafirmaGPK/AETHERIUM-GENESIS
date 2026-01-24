from typing import Dict, Any, Optional
import re
from .logenesis_schemas import (
    LogenesisResponse, LogenesisState, IntentVector,
    VisualQualia, PhysicsParams
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
            emotional_load=0.1,
            decision_urgency=0.1,
            precision_required=0.1
        )

        # Keyword Heuristics
        if any(w in text for w in ["search", "find", "what", "how", "define", "ค้นหา", "คือ"]):
            vector.epistemic_need = 0.9
            vector.precision_required = 0.7

        if any(w in text for w in ["sad", "feel", "worry", "love", "hate", "tired", "เศร้า", "เหนื่อย"]):
            vector.emotional_load = 0.9
            vector.epistemic_need = 0.2

        if any(w in text for w in ["analyze", "code", "debug", "structure", "plan", "วิเคราะห์", "โครงสร้าง"]):
            vector.precision_required = 0.95
            vector.epistemic_need = 0.8

        if any(w in text for w in ["now", "urgent", "quick", "asap", "fast", "ด่วน", "เร็ว"]):
            vector.decision_urgency = 0.9
            vector.precision_required = 0.5

        return vector

class LogenesisEngine:
    """
    The Adaptive Resonance Engine.
    Manages state (Awake/Nirodha) and generates holistic responses.
    """
    def __init__(self):
        self.state = LogenesisState.VOID
        self.intent_extractor = MockIntentExtractor()

    def process(self, text: str) -> LogenesisResponse:
        # Check for Nirodha Triggers (The "Silence Protocol")
        if any(w in text.lower() for w in ["sleep", "stop", "rest", "retreat", "bye", "enough", "พอ", "พัก"]):
            return self.enter_nirodha()

        # If currently in VOID or NIRODHA, wake up
        if self.state != LogenesisState.AWAKENED:
            self.state = LogenesisState.AWAKENED

        # 1. Intent Extraction
        intent = self.intent_extractor.extract(text)

        # 2. Resonance Calculation (Determine the "Qualia")
        qualia = self._calculate_qualia(intent)
        physics = self._calculate_physics(intent)

        # 3. Synthesize Text Response (Mocked based on intent)
        response_text = self._synthesize_text(intent)

        return LogenesisResponse(
            state=self.state,
            text_content=response_text,
            visual_qualia=qualia,
            physics_params=physics,
            intent_debug=intent
        )

    def enter_nirodha(self) -> LogenesisResponse:
        """
        Executes the 'Peaceful Retreat'.
        Clears context and fades visuals to black.
        """
        self.state = LogenesisState.NIRODHA

        return LogenesisResponse(
            state=LogenesisState.NIRODHA,
            text_content="Entering Nirodha state. Resting...",
            visual_qualia=VisualQualia(
                color="#050505",  # Void Black
                intensity=0.0,
                turbulence=0.0,
                shape="void"
            ),
            physics_params=PhysicsParams(
                spawn_rate=0,
                velocity_bias=[0.0, 0.0],
                decay_rate=0.1 # Fast fade
            )
        )

    def _calculate_qualia(self, intent: IntentVector) -> VisualQualia:
        # Logic to map Intent -> Visuals

        # Default: Gentle White/Grey
        color = "#e0e0e0"
        intensity = 0.5
        turbulence = 0.1
        shape = "nebula"

        if intent.emotional_load > 0.6:
            color = "#A855F7" # Purple (Empathy)
            intensity = 0.8
            turbulence = 0.2
            shape = "nebula"

        elif intent.precision_required > 0.6:
            color = "#06b6d4" # Cyan (Logic/Structure)
            intensity = 0.9
            turbulence = 0.05 # Very stable
            shape = "shard" # Crystalline

        elif intent.decision_urgency > 0.6:
            color = "#f59e0b" # Amber (Alert)
            intensity = 1.0
            turbulence = 0.8 # High energy
            shape = "orb"

        return VisualQualia(
            color=color,
            intensity=intensity,
            turbulence=turbulence,
            shape=shape
        )

    def _calculate_physics(self, intent: IntentVector) -> PhysicsParams:
        # Map Intent -> Particle Physics
        spawn_rate = 2
        decay = 0.01

        if intent.emotional_load > 0.5:
            spawn_rate = 5
            decay = 0.005 # Long lasting trails

        if intent.decision_urgency > 0.5:
            spawn_rate = 20 # Burst
            decay = 0.05 # Fast fade

        return PhysicsParams(
            spawn_rate=spawn_rate,
            decay_rate=decay
        )

    def _synthesize_text(self, intent: IntentVector) -> str:
        # Simple mock responses based on dominant vector component

        if intent.emotional_load > 0.6:
            return "I sense a weight in your words. I am here to listen. Please, tell me more."

        if intent.epistemic_need > 0.6:
            return f"Accessing knowledge base... Analyzing request with precision {intent.precision_required*100:.0f}%. Here is the structured data you requested."

        if intent.decision_urgency > 0.6:
            return "Immediate action required. Initiating rapid response protocol."

        return "I am LOGENESIS. My logic is fluid, my state is resonant. How may I adapt to you today?"
