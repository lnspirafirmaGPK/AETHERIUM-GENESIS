from pydantic import BaseModel
from typing import Optional, Tuple, List, Dict
from enum import Enum, IntEnum

class LightAction(str, Enum):
    SPAWN = "SPAWN"
    MOVE = "MOVE"
    ERASE = "ERASE"
    EMPHASIZE = "EMPHASIZE"

class TemporalType(str, Enum):
    INSTANT = "instant"
    CONTINUOUS = "continuous"

class PriorityLevel(IntEnum):
    AMBIENT = 0
    USER = 1
    SAFETY = 2
    SYSTEM = 3

class LightIntent(BaseModel):
    action: LightAction
    target: Optional[str] = None
    region: Optional[Tuple[float, float, float, float]] = None # normalized bbox
    vector: Optional[Tuple[float, float]] = None # direction
    intensity: Optional[float] = None
    color_hint: Optional[str] = None
    decay: Optional[float] = None
    temporal: Optional[TemporalType] = None
    priority: int = PriorityLevel.USER
    source: str = "unknown"

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
    text_content: Optional[str] = None

class LightEntity(BaseModel):
    id: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    energy: float
    history: List[Tuple[float, float]] = []

class LightState(BaseModel):
    entities: Dict[str, LightEntity]
    system_energy: float
