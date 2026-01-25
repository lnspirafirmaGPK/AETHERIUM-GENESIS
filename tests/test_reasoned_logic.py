import sys
import os
import pytest
from src.backend.core.logenesis_engine import LogenesisEngine
from src.backend.core.logenesis_schemas import LogenesisResponse, IntentVector, AudioQualia

def test_reasoned_response_subjective():
    engine = LogenesisEngine()

    # Input that should trigger subjective weight
    response = engine.process("I am worried about the market risk")

    # 1. Check Schema Compliance
    assert isinstance(response, LogenesisResponse)
    assert response.audio_qualia is not None
    assert isinstance(response.audio_qualia, AudioQualia)

    # 2. Check Intent Extraction (Subjective Weight)
    # The MockIntentExtractor should set subjective_weight high for "worried" / "risk"
    assert response.intent_debug.subjective_weight > 0.6

    # 3. Check Reasoned Text Response
    # Should NOT be "I sense a weight..."
    # Should BE "Subjective density detected..."
    assert "Subjective density detected" in response.text_content
    assert "risk vectors" in response.text_content
    assert "feel" not in response.text_content.lower() # Ensure no emotional mirroring

def test_reasoned_response_epistemic():
    engine = LogenesisEngine()

    # Input that should trigger epistemic need (search/analyze)
    response = engine.process("Analyze the structure of this code")

    assert response.intent_debug.epistemic_need > 0.6
    assert response.intent_debug.precision_required > 0.6

    # Check Text
    assert "Query processing complete" in response.text_content
    assert "Precision alignment" in response.text_content

def test_nirodha_audio():
    engine = LogenesisEngine()

    # Trigger Nirodha
    response = engine.process("Rest now, enough")

    assert response.state == "NIRODHA"
    # Audio should be silent/minimal
    assert response.audio_qualia.rhythm_density == 0.0
    assert response.audio_qualia.amplitude_bias == 0.0

if __name__ == "__main__":
    # Manually run if executed as script
    try:
        test_reasoned_response_subjective()
        test_reasoned_response_epistemic()
        test_nirodha_audio()
        print("ALL TESTS PASSED")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
