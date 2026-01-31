import numpy as np
import logging
from ..core.correction_schemas import CorrectionEvent, CorrectionAction, StructuralGuide

logger = logging.getLogger(__name__)

TORCH_AVAILABLE = False
try:
    import torch
    from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, DDIMScheduler
    from ..core.region_extractor import RegionExtractor
    TORCH_AVAILABLE = True
except ImportError:
    logger.warning("AdvancedDiffusion disabled due to missing torch/diffusers dependencies.")

    # Mock classes to prevent NameErrors if code references them
    class ControlNetModel:
        @classmethod
        def from_pretrained(cls, *args, **kwargs): return None
    class StableDiffusionControlNetPipeline:
        @classmethod
        def from_pretrained(cls, *args, **kwargs): return None
    class DDIMScheduler:
        @classmethod
        def from_config(cls, *args, **kwargs): return None
    class RegionExtractor:
        def __init__(self, *args, **kwargs): pass
        def extract(self, *args, **kwargs): return None
        def merge(self, *args, **kwargs): return None

class AdvancedDiffusion:
    def __init__(self, device: str = "cuda"):
        if not TORCH_AVAILABLE:
            self.device = "cpu"
            self.pipe = None
            self.extractor = None
            return

        if not torch.cuda.is_available() and device == "cuda":
            device = "cpu"

        self.device = device
        # Note: In a real environment, this downloads models.
        # In this sandbox, we might need to mock this for tests.
        try:
            self.controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-tile")
            self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", controlnet=self.controlnet
            ).to(self.device)
            self.pipe.scheduler = DDIMScheduler.from_config(self.pipe.scheduler.config)
        except Exception as e:
             logger.error(f"Failed to load diffusion models: {e}")
             self.pipe = None

        self.extractor = None

    def set_frame_shape(self, shape):
        if TORCH_AVAILABLE:
            self.extractor = RegionExtractor(shape)

    def select_controlnet(self, event: CorrectionEvent) -> StructuralGuide:
        if event.action_type in [CorrectionAction.MOVE, CorrectionAction.REDRAW]:
            return StructuralGuide.TILE
        if event.action_type == CorrectionAction.LOCK:
            return StructuralGuide.EDGE
        return StructuralGuide.TILE

    def regenerate(
        self,
        full_frame: "torch.Tensor",
        event: CorrectionEvent,
        current_time: float
    ) -> "torch.Tensor":
        if not TORCH_AVAILABLE or self.pipe is None:
            return full_frame

        if self.extractor is None:
            raise RuntimeError("Frame shape not set")

        # In a full implementation, we would switch models based on:
        # guide = self.select_controlnet(event)

        region = self.extractor.extract(full_frame, event.affected_region)
        if region is None: return full_frame

        # Create condition for ControlNet (Tile)
        # Using mean to simplify logic as per design pattern
        condition = region.mean(dim=0, keepdim=True).repeat(1, 3, 1, 1)

        elapsed = current_time - event.timestamp
        decay = 1.0
        if event.mode == "short_decay":
            # half_life = 0.75s
            decay = max(0.0, 0.5 ** (elapsed / 0.75)) if elapsed < 2.0 else 0.0

        strength = decay
        if len(event.intent_vector) > 2:
            strength *= event.intent_vector[2]

        # Run inference
        result = self.pipe(
            prompt="",
            image=condition,
            controlnet_conditioning_scale=strength,
            num_inference_steps=16,
            guidance_scale=5.0
        ).images[0]

        # Convert result (PIL Image) to Tensor
        # result is (W, H) PIL Image
        arr = np.array(result)
        # arr is (H, W, 3)
        updated_region = torch.from_numpy(arr).permute(2, 0, 1).to(full_frame.device)

        # Ensure dtype match
        if full_frame.dtype.is_floating_point and not updated_region.dtype.is_floating_point:
             updated_region = updated_region.float()
             # If full_frame is normalized [0,1], we might need to normalize updated_region [0,255] -> [0,1]
             # But we assume consistency in usage for now or that full_frame is [0, 255] float.

        return self.extractor.merge(full_frame, updated_region, event.affected_region)
