import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from src.backend.server import app

def verify_gunui_integration():
    print("Connecting to WebSocket...")
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        # 1. Test INTENT_START
        print("Sending INTENT_START...")
        websocket.send_json({"type": "INTENT_START", "meta": {"ts": 123456789}})
        data = websocket.receive_json()
        print(f"Received: {data}")
        assert data["type"] == "ACK"
        assert data["for"] == "INTENT_START"

        # 2. Test INTENT_END (Simulate Actuator Release)
        print("Sending INTENT_END...")
        websocket.send_json({"type": "INTENT_END", "meta": {"duration": 1500}})

        # Expect VISUAL_PARAMS
        data_visual = websocket.receive_json()
        print(f"Received: {data_visual['type']}")
        assert data_visual["type"] == "VISUAL_PARAMS"
        assert "params" in data_visual

        # Expect AI_SPEAK
        data_speak = websocket.receive_json()
        print(f"Received: {data_speak['type']}")
        assert data_speak["type"] == "AI_SPEAK"
        assert "text" in data_speak

        print("\n[SUCCESS] GunUI Protocol Verified: Start -> End -> Visuals -> TTS")

if __name__ == "__main__":
    verify_gunui_integration()
