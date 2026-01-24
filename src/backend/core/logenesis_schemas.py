from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class LogenesisState(str, Enum):
    VOID = "VOID"
    AWAKENED = "AWAKENED"
    NIRODHA = "NIRODHA"

class IntentVector(BaseModel):
    """
    Mathematical representation of the user's latent intent.
    Used by ARL (Adaptive Resonance Logic) to calculate resonance scores.
    """
    epistemic_need: float = Field(..., description="Need for raw knowledge/facts (0.0-1.0)")
    emotional_load: float = Field(..., description="Need for emotional support/listening (0.0-1.0)")
    decision_urgency: float = Field(..., description="Need for immediate decision/action (0.0-1.0)")
    precision_required: float = Field(..., description="Need for precise/formal structure (0.0-1.0)")
    # Simulation of high-dimensional embedding
    raw_embedding: Optional[List[float]] = Field(default=None, description="Mock 512-dim vector")

class VisualQualia(BaseModel):
    """
    Non-verbal communication parameters (The 'Light' Language).
    """
    color: str = Field(..., description="Hex color code, e.g., #A855F7")
    intensity: float = Field(..., description="Brightness/Opacity (0.0-1.0)")
    turbulence: float = Field(..., description="Chaos factor: 0.0=Still, 1.0=Violent Storm")
    shape: str = Field(default="nebula", description="Target shape topology: nebula, shard, orb, void")

class PhysicsParams(BaseModel):
    """
    Direct instructions for the GunUI particle engine.
    """
    spawn_rate: int = Field(default=0, description="Particles to spawn per frame/tick")
    velocity_bias: List[float] = Field(default_factory=lambda: [0.0, 0.0], description="[x, y] flow bias")
    decay_rate: float = Field(default=0.01, description="How fast particles fade")

class LogenesisResponse(BaseModel):
    """
    The holistic response packet from LOGENESIS Engine.
    Combines verbal (text) and non-verbal (visual/physics) signals.
    """
    type: str = "LOGENESIS_RESPONSE"
    state: LogenesisState
    text_content: Optional[str] = None
    visual_qualia: Optional[VisualQualia] = None
    physics_params: Optional[PhysicsParams] = None
    intent_debug: Optional[IntentVector] = None  # For testbed visualization
