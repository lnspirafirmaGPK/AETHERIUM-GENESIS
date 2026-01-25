import asyncio
from typing import Dict, Any, Optional
from .intent_interpreter import IntentInterpreter
from .visual_schemas import VisualParameters, IntentCategory, BaseShape, VisualSpecifics

class SimulatedIntentInterpreter(IntentInterpreter):
    """
    A deterministic interpreter for testing and fallback.
    Maps keywords to specific VisualParameters.
    """

    async def interpret(self, text: str, context: Optional[Dict[str, Any]] = None) -> VisualParameters:
        text = text.lower()

        # Default State (Neutral / Nebula)
        category = IntentCategory.CHAT
        valence = 0.1
        energy = 0.3
        shape = BaseShape.CLOUD
        color = "#FFFFFF" # White
        turbulence = 0.1
        density = 0.5
        concepts = []

        # 1. Detect Category
        if any(w in text for w in ["search", "find", "analyze", "check", "what", "how"]):
            category = IntentCategory.REQUEST
            energy = 0.6
            concepts.append("inquiry")
        elif any(w in text for w in ["stop", "start", "reset", "clear", "move", "make"]):
            category = IntentCategory.COMMAND
            energy = 0.8
            concepts.append("control")
        elif any(w in text for w in ["error", "fail", "broken", "bug", "crash"]):
            category = IntentCategory.ERROR
            valence = -0.8
            energy = 0.9
            concepts.append("failure")

        # 2. Detect Keywords for Visuals

        # Shapes
        if any(w in text for w in ["circle", "sphere", "round", "ball", "orb"]):
            shape = BaseShape.SPHERE
            concepts.append("unity")
        elif any(w in text for w in ["box", "cube", "square", "structure", "logic"]):
            shape = BaseShape.CUBE
            concepts.append("structure")
            color = "#00FFFF" # Cyan
        elif any(w in text for w in ["spiral", "vortex", "deep", "think", "wisdom"]):
            shape = BaseShape.VORTEX
            concepts.append("wisdom")
            color = "#800080" # Purple
        elif any(w in text for w in ["crack", "error", "fail", "broken"]):
            shape = BaseShape.CRACKS
            concepts.append("fragility")
            color = "#FF4500" # OrangeRed
        elif any(w in text for w in ["scatter", "chaos", "reset"]):
            shape = BaseShape.SCATTER
            turbulence = 1.0

        # Colors (Explicit override)
        if "red" in text: color = "#FF0000"; valence = -0.5
        if "blue" in text: color = "#0000FF"; valence = 0.5
        if "green" in text: color = "#00FF00"; valence = 0.8
        if "purple" in text: color = "#800080"
        if "gold" in text or "yellow" in text: color = "#FFD700"; energy = 0.9

        # Intensity
        if "urgent" in text or "fast" in text:
            energy = 1.0
            turbulence = 0.8
        if "calm" in text or "slow" in text:
            energy = 0.1
            turbulence = 0.0

        return VisualParameters(
            intent_category=category,
            emotional_valence=valence,
            energy_level=energy,
            semantic_concepts=concepts,
            visual_parameters=VisualSpecifics(
                base_shape=shape,
                turbulence=turbulence,
                particle_density=density,
                color_palette=color,
                flow_direction="inward" if shape == BaseShape.VORTEX else "none"
            )
        )
