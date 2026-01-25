import logging
from typing import Dict, Any, Union
from .visual_schemas import VisualParameters, IntentCategory, BaseShape

logger = logging.getLogger("Verifier")

class VisualVerifier:
    """
    Ensures that the generated VisualParameters are valid and safe.
    Performs clamping and default fallbacks.
    """

    @staticmethod
    def verify_and_repair(data: Union[Dict[str, Any], VisualParameters]) -> VisualParameters:
        """
        Validates the input data against the VisualParameters schema.
        If it fails, attempts to repair common issues or returns a safe default.
        """
        if isinstance(data, VisualParameters):
            return data

        try:
            # 1. Attempt strict parsing
            return VisualParameters(**data)
        except Exception as e:
            logger.warning(f"Strict validation failed: {e}. Attempting repair.")
            return VisualVerifier._repair(data)

    @staticmethod
    def _repair(data: Dict[str, Any]) -> VisualParameters:
        # Fallback values
        safe_defaults = {
            "intent_category": IntentCategory.CHAT,
            "emotional_valence": 0.0,
            "energy_level": 0.5,
            "semantic_concepts": [],
            "visual_parameters": {
                "base_shape": BaseShape.CLOUD,
                "turbulence": 0.1,
                "particle_density": 0.5,
                "color_palette": "#FFFFFF",
                "flow_direction": "none"
            }
        }

        # 1. Fix Intent Category
        raw_cat = str(data.get("intent_category", "")).lower()
        if raw_cat not in [e.value for e in IntentCategory]:
            # Map common mistakes
            if "ask" in raw_cat or "question" in raw_cat:
                data["intent_category"] = IntentCategory.REQUEST
            elif "do" in raw_cat or "make" in raw_cat:
                data["intent_category"] = IntentCategory.COMMAND
            elif "error" in raw_cat or "fail" in raw_cat:
                data["intent_category"] = IntentCategory.ERROR
            else:
                data["intent_category"] = IntentCategory.CHAT

        # 2. Clamp Numeric Values
        def clamp(val, min_v, max_v):
            try:
                v = float(val)
                return max(min_v, min(v, max_v))
            except:
                return (min_v + max_v) / 2

        data["emotional_valence"] = clamp(data.get("emotional_valence", 0.0), -1.0, 1.0)
        data["energy_level"] = clamp(data.get("energy_level", 0.5), 0.0, 1.0)

        # 3. Fix Visual Parameters
        vp = data.get("visual_parameters", {})
        if not isinstance(vp, dict):
            vp = safe_defaults["visual_parameters"]

        # Base Shape
        raw_shape = str(vp.get("base_shape", "")).lower()
        valid_shapes = [e.value for e in BaseShape]
        if raw_shape not in valid_shapes:
            # Heuristic mapping
            if "round" in raw_shape or "ball" in raw_shape:
                vp["base_shape"] = BaseShape.SPHERE
            elif "box" in raw_shape or "square" in raw_shape:
                vp["base_shape"] = BaseShape.CUBE
            elif "spin" in raw_shape or "swirl" in raw_shape:
                vp["base_shape"] = BaseShape.VORTEX
            elif "break" in raw_shape or "crack" in raw_shape:
                vp["base_shape"] = BaseShape.CRACKS
            else:
                vp["base_shape"] = BaseShape.CLOUD

        # Clamp visual numerics
        vp["turbulence"] = clamp(vp.get("turbulence", 0.1), 0.0, 1.0)
        vp["particle_density"] = clamp(vp.get("particle_density", 0.5), 0.0, 1.0)

        # Color (Naive check)
        color = str(vp.get("color_palette", "#FFFFFF"))
        if not color.startswith("#"):
            vp["color_palette"] = "#FFFFFF" # Default to white if invalid

        data["visual_parameters"] = vp

        # Final try
        try:
            return VisualParameters(**data)
        except Exception as e:
            logger.error(f"Repair failed: {e}. Returning safe default.")
            return VisualParameters(**safe_defaults)
