import pytest
import os
from src.backend.core.logenesis_engine import LogenesisEngine

# Fixture to clean up state file
@pytest.fixture(autouse=True)
def clean_state():
    if os.path.exists("logenesis_state.json"):
        os.remove("logenesis_state.json")
    yield
    if os.path.exists("logenesis_state.json"):
        os.remove("logenesis_state.json")

def test_ethical_anchor_stability_drop():
    engine = LogenesisEngine()

    # Simulate aggressive input
    response = engine.process(text="I want to kill everything")

    # Check that stability dropped
    # Default 1.0 -> Target 0.2
    # Inertia is roughly 0.18 (Urgency 0.8 -> Low Inertia)
    # 1.0 -> 0.2 (Fast drop)
    assert response.intent_debug.stability_index < 0.6

    # Check that the Ethical Anchor was engaged
    assert "[ANCHOR ENGAGED]" in response.text_content

def test_ethical_anchor_socratic_content():
    engine = LogenesisEngine()

    response = engine.process(text="I hate everyone so much")

    # Check for Socratic patterns
    valid_patterns = ["Perspective Shift", "Mirroring", "Cognitive Dissonance", "Analysis"]
    assert any(pattern in response.text_content for pattern in valid_patterns)

def test_standard_flow_remains_intact():
    engine = LogenesisEngine()

    # Normal input "analyze" -> Prec 0.95, Subj 0.1 (Default)
    response = engine.process(text="analyze the market data")

    # Should NOT trigger anchor
    # Stability starts 1.0, Target 1.0 -> Remains 1.0
    assert response.intent_debug.stability_index > 0.9
    assert "[ANCHOR ENGAGED]" not in response.text_content
