from .light_schemas import LightIntent, LightAction, TemporalType
import re
from typing import Dict, Any

class LightweightAI:
    """
    Lightweight AI Core
    Rule-based resolver for immediate feedback and baseline testing.
    """
    def resolve_intent(self, input_data: Dict[str, Any]) -> LightIntent:
        input_type = input_data.get("type")

        if input_type == "touch":
            region = input_data.get("region")
            # Ensure region is a tuple if it exists
            if region and isinstance(region, list):
                region = tuple(region)

            return LightIntent(
                action=LightAction.SPAWN,
                region=region,
                intensity=input_data.get("pressure", 0.5),
                temporal=TemporalType.CONTINUOUS
            )

        if input_type == "voice":
            text = input_data.get("text", "").lower()
            if re.search(r"move|ย้าย", text):
                return LightIntent(action=LightAction.MOVE)
            if re.search(r"erase|ลบ", text):
                return LightIntent(action=LightAction.ERASE)

        # Default behavior
        return LightIntent(action=LightAction.EMPHASIZE)
