import pytest
from src.backend.core.logenesis_engine import LogenesisEngine
from src.backend.core.light_schemas import LightAction

def test_explicit_command_bypass():
    """
    Verify that explicit commands still work and bypass the gate logic
    (or are handled by the parser first).
    """
    engine = LogenesisEngine()

    # "circle" should trigger explicit parser
    response = engine.process("Make a circle")

    assert response.light_intent is not None
    assert response.light_intent.action == LightAction.MANIFEST
    assert response.light_intent.shape_name == "circle"

def test_neutral_conversation_no_manifest():
    """
    Verify that low-intensity conversation does NOT trigger manifestation.
    """
    engine = LogenesisEngine()

    # Neutral/Low intensity input
    response = engine.process("Hello, how are you?")

    # Should be None unless the engine starts with high random drift,
    # but default state is usually neutral.
    assert response.light_intent is None

def test_manifestation_gate_subjective():
    """
    Verify that high subjective intensity triggers 'spiral'.
    We mix in some urgency ('now') to lower inertia and speed up the test,
    otherwise drifting from 0.1 to 0.8 with 0.95 inertia takes too long.
    """
    engine = LogenesisEngine()

    # "sad" -> Subjective=0.9
    # "now" -> Urgency=0.9 (Lowers inertia)
    input_text = "I feel extremely sad now."

    # Loop to drift state
    triggered = False
    for _ in range(10):
        response = engine.process(input_text, session_id="test_sub")
        if response.light_intent:
            # Verify it picked the right dominant trait
            # Since we added "now", urgency is also high.
            # Logic: if subjective >= max_intensity.
            # If subjective=0.9 and urgency=0.9, max is 0.9.
            # Check logic order: Precision -> Subjective -> Urgency.
            # So Subjective checks first. It should win if equal.
            if response.light_intent.shape_name == "spiral":
                triggered = True
                break

    assert triggered, "Did not trigger manifestation for high subjective load"
    assert response.light_intent.action == LightAction.MANIFEST
    assert response.light_intent.shape_name == "spiral"

def test_manifestation_gate_precision():
    """
    Verify that high precision intensity triggers 'square'.
    """
    engine = LogenesisEngine()

    # "analyze" -> Precision=0.95
    # "now" -> Urgency=0.9 (Lowers inertia)
    input_text = "Analyze the code now."

    triggered = False
    for _ in range(10):
        response = engine.process(input_text, session_id="test_prec")
        if response.light_intent:
            if response.light_intent.shape_name == "square":
                triggered = True
                break

    assert triggered, "Did not trigger manifestation for high precision load"
    assert response.light_intent.shape_name == "square"

def test_manifestation_gate_urgency():
    """
    Verify that high urgency intensity triggers 'circle'.
    """
    engine = LogenesisEngine()

    # "now", "urgent", "quick" -> Urgency=0.9
    # No other keywords, so subjective/precision stay low.
    input_text = "Do it now! Urgent! Quick!"

    triggered = False
    for _ in range(10):
        response = engine.process(input_text, session_id="test_urg")
        if response.light_intent:
            triggered = True
            break

    assert triggered, "Did not trigger manifestation for high urgency"
    assert response.light_intent.shape_name == "circle"

def test_manifestation_gate_epistemic():
    """
    Verify that high epistemic need triggers 'line'.
    """
    engine = LogenesisEngine()

    # "search", "find" -> Epistemic=0.9
    # "now" -> Urgency=0.9
    input_text = "Find the answer now."

    triggered = False
    for _ in range(10):
        response = engine.process(input_text, session_id="test_epi")
        if response.light_intent:
             # Epistemic checked last in my implementation logic?
             # Let's check logic: Precision -> Subjective -> Urgency -> Epistemic.
             # If Epistemic is high, but Urgency is also high (due to 'now'), Urgency might win because it's checked earlier?
             # Wait, logic is:
             # if precision >= max: ...
             # elif subjective >= max: ...
             # elif urgency >= max: ...
             # elif epistemic >= max: ...

             # If epistemic=0.9 and urgency=0.9. Max=0.9.
             # Urgency is checked before Epistemic. So it will return Circle.
             # This is a flaw in my test design or logic.
             # To test Epistemic, I need Epistemic to be strictly higher than others.
             # But without "now", inertia is high.
             # I should just iterate more times without "now".
             pass

    # Retry with pure epistemic input (slower drift)
    input_text_pure = "Search find what define"

    triggered = False
    for _ in range(30): # Give it more time to drift
        response = engine.process(input_text_pure, session_id="test_epi_pure")
        if response.light_intent:
            triggered = True
            break

    assert triggered, "Did not trigger manifestation for high epistemic"
    assert response.light_intent.shape_name == "line"
