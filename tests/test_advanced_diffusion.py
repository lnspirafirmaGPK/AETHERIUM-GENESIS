import pytest
import torch
from unittest.mock import MagicMock, patch
from src.backend.private.advanced_diffusion import AdvancedDiffusion
from src.backend.genesis_core.logenesis.correction_schemas import CorrectionEvent, SpatialMask, CorrectionAction, StructuralGuide
from PIL import Image

@pytest.fixture
def mock_diffusion_components():
    with patch('src.backend.private.advanced_diffusion.ControlNetModel.from_pretrained') as mock_cn, \
         patch('src.backend.private.advanced_diffusion.StableDiffusionControlNetPipeline.from_pretrained') as mock_pipe, \
         patch('src.backend.private.advanced_diffusion.DDIMScheduler.from_config') as mock_sched:

        # Setup mock pipeline
        mock_instance = MagicMock()
        mock_pipe.return_value = mock_instance

        # Mock .to() call to return the same instance (since constructor calls .to(device))
        mock_instance.to.return_value = mock_instance

        # Mock the pipe call return
        mock_output = MagicMock()
        # Create a real small image to be compatible with np.array()
        # The region size in test is 10x10
        mock_output.images = [Image.new('RGB', (10, 10), color='red')]
        mock_instance.return_value = mock_output
        mock_instance.scheduler.config = {}

        yield mock_instance

def test_select_controlnet(mock_diffusion_components):
    # Initialize without downloading models
    ad = AdvancedDiffusion(device="cpu")

    event_move = CorrectionEvent("1", "s1", 0.0, SpatialMask(0,0,10,10), CorrectionAction.MOVE, [], "short_decay")
    assert ad.select_controlnet(event_move) == StructuralGuide.TILE

    event_lock = CorrectionEvent("2", "s1", 0.0, SpatialMask(0,0,10,10), CorrectionAction.LOCK, [], "persistent")
    assert ad.select_controlnet(event_lock) == StructuralGuide.EDGE

def test_regenerate(mock_diffusion_components):
    ad = AdvancedDiffusion(device="cpu")
    ad.set_frame_shape((100, 100, 3))

    full_frame = torch.randn(3, 100, 100)
    event = CorrectionEvent(
        "1", "s1", 1000.0,
        SpatialMask(10, 10, 20, 20),
        CorrectionAction.MOVE,
        [1.0, 1.0, 0.8],
        "short_decay"
    )

    # We rely on mocks, so we just check if it runs without error and calls pipe
    result = ad.regenerate(full_frame, event, current_time=1000.1)

    assert result.shape == (3, 100, 100)
    mock_diffusion_components.assert_called_once()
