from enum import Enum
from dataclasses import dataclass
from typing import Any

class AetherState(Enum):
    IDLE = 0
    PERCEPTION = 1
    ANALYSIS = 2
    MANIFESTATION = 3
    STABILIZED = 4

@dataclass
class AetherOutput:
    light_field: Any # Was torch.Tensor
    embedding: Any # Was torch.Tensor
    energy_level: float
    confidence: float
    state: AetherState
