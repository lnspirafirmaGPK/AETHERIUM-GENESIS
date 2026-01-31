from enum import Enum
from dataclasses import dataclass
import torch

class AetherState(Enum):
    IDLE = 0
    PERCEPTION = 1
    ANALYSIS = 2
    MANIFESTATION = 3
    STABILIZED = 4

@dataclass
class AetherOutput:
    light_field: torch.Tensor
    embedding: torch.Tensor
    energy_level: float
    confidence: float
    state: AetherState
