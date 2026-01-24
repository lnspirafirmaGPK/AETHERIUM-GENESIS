from .light_schemas import LightIntent, LightInstruction, LightAction

class LightControlLogic:
    """
    Light Control Logic (LCL)
    Translates abstract LightIntent into concrete LightInstruction for the renderer.
    Must be deterministic.
    """

    def process(self, intent: LightIntent) -> LightInstruction:
        if intent.action == LightAction.MOVE:
            return LightInstruction(
                intent=LightAction.MOVE,
                target=intent.target or "GLOBAL",
                vector=intent.vector or (0.0, 0.0),
                strength=intent.intensity if intent.intensity is not None else 0.8,
                decay=intent.decay if intent.decay is not None else 0.9
            )
        elif intent.action == LightAction.SPAWN:
            return LightInstruction(
                intent=LightAction.SPAWN,
                shape="organic", # Default deterministic choice
                region=intent.region or (0.0, 0.0, 1.0, 1.0),
                motion="flow",
                color_profile=intent.color_hint or "natural_green"
            )
        elif intent.action == LightAction.ERASE:
            return LightInstruction(
                intent=LightAction.ERASE,
                target=intent.target,
                region=intent.region,
                strength=1.0
            )
        elif intent.action == LightAction.EMPHASIZE:
             return LightInstruction(
                intent=LightAction.EMPHASIZE,
                target=intent.target,
                strength=intent.intensity or 1.0,
                color_profile=intent.color_hint or "bright"
            )

        # Fallback
        return LightInstruction(intent=LightAction.EMPHASIZE, strength=0.0)
