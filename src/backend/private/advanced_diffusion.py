import torch
import numpy as np
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, DDIMScheduler
from ..core.region_extractor import RegionExtractor
from ..core.correction_schemas import CorrectionEvent, CorrectionAction, StructuralGuide

class AdvancedDiffusion:
    def __init__(self, device: str = "cuda"):
        if not torch.cuda.is_available() and device == "cuda":
            device = "cpu"

        self.device = device
        # Note: In a real environment, this downloads models.
        # In this sandbox, we might need to mock this for tests.
        self.controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-tile")
        self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5", controlnet=self.controlnet
        ).to(self.device)
        self.pipe.scheduler = DDIMScheduler.from_config(self.pipe.scheduler.config)
        self.extractor = None

    def set_frame_shape(self, shape):
        self.extractor = RegionExtractor(shape)

    def select_controlnet(self, event: CorrectionEvent) -> StructuralGuide:
        if event.action_type in [CorrectionAction.MOVE, CorrectionAction.REDRAW]:
            return StructuralGuide.TILE
        if event.action_type == CorrectionAction.LOCK:
            return StructuralGuide.EDGE
        return StructuralGuide.TILE

    def regenerate(
        self,
        full_frame: torch.Tensor,
        event: CorrectionEvent,
        current_time: float
    ) -> torch.Tensor:
        if self.extractor is None:
            raise RuntimeError("Frame shape not set")

        # In a full implementation, we would switch models based on:
        # guide = self.select_controlnet(event)

        region = self.extractor.extract(full_frame, event.affected_region)

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
