import sys
import os
import pytest
from dataclasses import FrozenInstanceError

# Add project root to sys.path to allow imports from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.core.schemas import CorrectionAction, SpatialMask, CorrectionEvent

def test_correction_action_enum():
    assert CorrectionAction.MOVE.value == "move"
    assert CorrectionAction.ERASE.value == "erase"
    assert CorrectionAction.REDRAW.value == "redraw"
    assert CorrectionAction.EMPHASIZE.value == "emphasize"

def test_spatial_mask_creation():
    mask = SpatialMask(x_min=0.0, y_min=0.0, x_max=10.0, y_max=10.0)
    assert mask.x_min == 0.0
    assert mask.y_max == 10.0

def test_spatial_mask_immutability():
    mask = SpatialMask(x_min=0.0, y_min=0.0, x_max=10.0, y_max=10.0)
    with pytest.raises(FrozenInstanceError):
        mask.x_min = 5.0

def test_correction_event_creation():
    mask = SpatialMask(x_min=0.0, y_min=0.0, x_max=10.0, y_max=10.0)
    event = CorrectionEvent(
        event_id="test-uuid",
        session_id="session-123",
        timestamp=1234567890.0,
        affected_region=mask,
        action_type=CorrectionAction.MOVE,
        intent_vector=[1.0, 2.0, 0.5, 100.0],
        previous_state_hash="hash123"
    )

    assert event.event_id == "test-uuid"
    assert event.action_type == CorrectionAction.MOVE
    assert event.affected_region.x_min == 0.0
    assert event.intent_vector == [1.0, 2.0, 0.5, 100.0]

def test_correction_event_optional_hash():
    mask = SpatialMask(x_min=0.0, y_min=0.0, x_max=10.0, y_max=10.0)
    event = CorrectionEvent(
        event_id="test-uuid-2",
        session_id="session-456",
        timestamp=1234567890.0,
        affected_region=mask,
        action_type=CorrectionAction.ERASE,
        intent_vector=[],
        previous_state_hash=None
    )
    assert event.previous_state_hash is None
