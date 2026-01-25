from typing import Dict, Any, Optional
import re
from .logenesis_schemas import (
    LogenesisResponse, LogenesisState, IntentVector,
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
        audio = self._calculate_audio(intent)
        physics = self._calculate_physics(intent)

        # 3. Synthesize Text Response (Reasoned Counterpart logic)
        response_text = self._synthesize_text(intent)

        return LogenesisResponse(
            state=self.state,
            text_content=response_text,
            visual_qualia=qualia,
            audio_qualia=audio,
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
        # Logic to map Intent -> Visuals

        # Default: Gentle White/Grey
        color = "#e0e0e0"
        intensity = 0.5
        turbulence = 0.1
        shape = "nebula"

        # High Subjective Weight -> Deep Color, Slower Turbulence (Thinking deeply about context)
        if intent.subjective_weight > 0.6:
            color = "#A855F7" # Deep Purple (Complexity/Context)
            intensity = 0.8
            turbulence = 0.3 # Moving, processing
            shape = "nebula"

        elif intent.precision_required > 0.6:
            color = "#06b6d4" # Cyan (Logic/Structure)
            intensity = 0.9
            turbulence = 0.05 # Very stable, crystalline
            shape = "shard"

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

    def _calculate_audio(self, intent: IntentVector) -> AudioQualia:
        # Default: Ambient, smooth
        rhythm = 0.1
        texture = "smooth"
        amp = 0.5

        if intent.decision_urgency > 0.6:
            rhythm = 0.9 # Rapid
            texture = "granular"
            amp = 0.9
        elif intent.subjective_weight > 0.6:
            rhythm = 0.2 # Slow, contemplative
            texture = "granular" # Complex texture
            amp = 0.6
        elif intent.precision_required > 0.8:
            rhythm = 0.5 # Steady
            texture = "smooth" # Clean
            amp = 0.7

        return AudioQualia(
            rhythm_density=rhythm,
            tone_texture=texture,
            amplitude_bias=amp
        )

    def _calculate_physics(self, intent: IntentVector) -> PhysicsParams:
        # Map Intent -> Particle Physics
        spawn_rate = 2
        decay = 0.01

        if intent.subjective_weight > 0.5:
            spawn_rate = 5
            decay = 0.005 # Long lasting trails, pondering

        if intent.decision_urgency > 0.5:
            spawn_rate = 20 # Burst
            decay = 0.05 # Fast fade

        return PhysicsParams(
            spawn_rate=spawn_rate,
            decay_rate=decay
        )

    def _synthesize_text(self, intent: IntentVector) -> str:
        """
        Generates the verbal response.
        PRINCIPLE: Reasoned Counterpart.
        - No emotional validation.
        - No persuasion.
        - Analytical, B2B, Structural.
        """

        # 1. Subjective/Emotional Input -> Reframe as Complexity/Risk
        if intent.subjective_weight > 0.6:
            # Reframe "feeling" or "worry" as "noise" or "complexity" to be managed.
            return "Subjective density detected. Recommending isolation of signal from noise to clarify risk vectors."

        # 2. Knowledge Request -> Professional Data Delivery
        if intent.epistemic_need > 0.6:
            return f"Query processing complete. Precision alignment: {intent.precision_required*100:.0f}%. Structured output follows."

        # 3. Urgency -> Action Protocol
        if intent.decision_urgency > 0.6:
            return "Latency critical. Immediate execution protocol initialized."

        # 4. Default State -> Availability
        return "System nominal. Ready for complex query integration."
