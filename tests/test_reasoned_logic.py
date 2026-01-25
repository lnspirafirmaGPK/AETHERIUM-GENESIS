import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from src.backend.core.logenesis_engine import LogenesisEngine
from src.backend.core.logenesis_schemas import LogenesisResponse, IntentVector, AudioQualia, ExpressionState

@pytest.fixture(autouse=True)
def mock_dependencies():
    """Mock StateStore to prevent side effects on the real file system."""
    with patch('src.backend.core.logenesis_engine.StateStore') as MockStore:
        mock_store_instance = MockStore.return_value
        # Default behavior for get_state: return neutral state
        mock_store_instance.get_state.return_value = ExpressionState(
            current_vector=IntentVector(
                epistemic_need=0.1, subjective_weight=0.1, decision_urgency=0.1, precision_required=0.1
            ),
            velocity=0.0,
            inertia=0.9
        )
        yield MockStore

def test_reasoned_response_subjective():
    # Patch _drift_state to bypass inertia and return input intent directly
    with patch.object(LogenesisEngine, '_drift_state') as mock_drift:
        engine = LogenesisEngine()

        target_vector = IntentVector(
            epistemic_need=0.4,
            subjective_weight=0.9,
            decision_urgency=0.1,
            precision_required=0.1
        )
        mock_drift.return_value = ExpressionState(
            current_vector=target_vector,
            velocity=1.0, # High velocity to bypass noise filter
            inertia=0.0
        )

        # Input that should trigger subjective weight
        response = engine.process("I am worried about the market risk")

        assert isinstance(response, LogenesisResponse)
        assert response.intent_debug.subjective_weight > 0.6
        assert "Signal weight acknowledged" in response.text_content

def test_reasoned_response_epistemic():
    with patch.object(LogenesisEngine, '_drift_state') as mock_drift:
        engine = LogenesisEngine()

        target_vector = IntentVector(
            epistemic_need=0.8,
            subjective_weight=0.1,
            decision_urgency=0.1,
            precision_required=0.95
        )
        mock_drift.return_value = ExpressionState(
            current_vector=target_vector,
            velocity=1.0, # Bypass noise filter
            inertia=0.0
        )

        response = engine.process("Analyze the structure of this code")

        assert response.intent_debug.epistemic_need > 0.6
        assert "Structure clear" in response.text_content

def test_nirodha_audio():
    engine = LogenesisEngine()
    response = engine.process("Rest now, enough")
    assert response.state == "NIRODHA"
    assert response.audio_qualia.rhythm_density == 0.0

if __name__ == "__main__":
    try:
        test_reasoned_response_subjective()
        test_reasoned_response_epistemic()
        test_nirodha_audio()
        print("ALL TESTS PASSED")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
