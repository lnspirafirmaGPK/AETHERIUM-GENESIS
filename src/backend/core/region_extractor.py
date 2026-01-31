from typing import Tuple, Any
from .correction_schemas import SpatialMask
import logging

logger = logging.getLogger(__name__)

try:
    import torch
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("Torch not available. RegionExtractor disabled.")

class RegionExtractor:
    def __init__(self, frame_shape: Tuple[int, int, int]):
        # Expecting (H, W, C)
        if len(frame_shape) == 3:
            self.h, self.w, _ = frame_shape
        else:
            self.h, self.w = 0, 0

    def validate(self, mask: SpatialMask) -> bool:
        try:
            return (0 <= mask.x_min < mask.x_max <= self.w) and (0 <= mask.y_min < mask.y_max <= self.h)
        except AttributeError:
            return False

    def extract(self, frame: Any, mask: SpatialMask) -> Any:
        """
        Extracts the region from the frame.
        Assumes frame is [C, H, W]
        """
        if not TORCH_AVAILABLE:
            return None

        if not self.validate(mask):
            raise ValueError("Mask out of bounds")
        return frame[:, mask.y_min:mask.y_max, mask.x_min:mask.x_max].clone()

    def merge(self, full: Any, updated_region: Any, mask: SpatialMask) -> Any:
        """
        Merges the updated region back into the full frame with a blend.
        Assumes full and updated_region are [C, H, W] (region dimensions for updated_region)
        """
        if not TORCH_AVAILABLE:
            return full

        x1, y1, x2, y2 = mask.x_min, mask.y_min, mask.x_max, mask.y_max

        # Create a horizontal blend mask (0 to 1)
        # Shape: (H_region, W_region)
        blend = torch.linspace(0, 1, steps=x2-x1).unsqueeze(0).expand(y2-y1, -1).to(full.device)

        full[:, y1:y2, x1:x2] = full[:, y1:y2, x1:x2] * (1 - blend) + updated_region * blend
        return full
