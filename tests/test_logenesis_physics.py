from fastapi.testclient import TestClient
from src.backend.server import app
from src.backend.core.logenesis_engine import LogenesisEngine
from src.backend.core.light_schemas import LightAction

client = TestClient(app)

def test_logenesis_physics_intent_detection():
    engine = LogenesisEngine()

    # Test Shape Detection
    response_circle = engine.process("Make a circle")
    assert response_circle.light_intent is not None
    assert response_circle.light_intent.action == LightAction.MANIFEST
    assert response_circle.light_intent.shape_name == "circle"

    # Test Movement Detection
    response_move = engine.process("Move left")
    assert response_move.light_intent is not None
    assert response_move.light_intent.action == LightAction.MOVE
    assert response_move.light_intent.vector == (-1.0, 0.0)

    # Test No Physics
    response_chat = engine.process("Hello world")
    assert response_chat.light_intent is None

def test_websocket_physics_integration():
    with client.websocket_connect("/ws") as websocket:
        # Simulate Logenesis Mode with a physics command
        payload = {
            "mode": "logenesis",
            "input": {
                "text": "Form a circle",
                "session_id": "test_session"
            }
        }
        websocket.send_json(payload)

        # Expect 1: Logenesis Response
        response1 = websocket.receive_json()
        assert response1["type"] == "LOGENESIS_RESPONSE"

        # Expect 2: Light Instruction (The Bridge result)
        response2 = websocket.receive_json()
        # The instruction is raw JSON, verify it has "intent": "MANIFEST" and formation data
        assert response2["intent"] == "MANIFEST"
        assert "formation_data" in response2
        assert len(response2["formation_data"]) > 0
