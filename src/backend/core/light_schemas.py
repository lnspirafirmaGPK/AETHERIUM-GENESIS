from pydantic import BaseModel
from typing import Optional, Tuple
from enum import Enum

class LightAction(str, Enum):
    SPAWN = "SPAWN"
    MOVE = "MOVE"
    ERASE = "ERASE"
    EMPHASIZE = "EMPHASIZE"

class TemporalType(str, Enum):
    INSTANT = "instant"
    CONTINUOUS = "continuous"

class LightIntent(BaseModel):
    action: LightAction
    target: Optional[str] = None
    region: Optional[Tuple[float, float, float, float]] = None # normalized bbox
    vector: Optional[Tuple[float, float]] = None # direction
    intensity: Optional[float] = None
    color_hint: Optional[str] = None
    decay: Optional[float] = None
    temporal: Optional[TemporalType] = None

class LightInstruction(BaseModel):
    intent: LightAction
    target: Optional[str] = None
    vector: Optional[Tuple[float, float]] = None
    strength: Optional[float] = None
    decay: Optional[float] = None
    shape: Optional[str] = None
    region: Optional[Tuple[float, float, float, float]] = None
    motion: Optional[str] = None
    color_profile: Optional[str] = None
