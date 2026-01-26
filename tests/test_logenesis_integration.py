from fastapi.testclient import TestClient
import sys
import os
import json

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.backend.server import app

client = TestClient(app)

def test_logenesis_flow():
    with client.websocket_connect("/ws") as websocket:
        # Test 1: Analyze (Precision)
        payload = {
            "mode": "logenesis",
            "input": {"text": "analyze system structure"}
        }

        response = None
        # Loop to overcome inertia
        for _ in range(3):
            websocket.send_text(json.dumps(payload))
            # Consume messages looking for LOGENESIS_RESPONSE
            for _ in range(5):
                data = websocket.receive_text()
                msg = json.loads(data)
                if msg.get("type") == "LOGENESIS_RESPONSE":
                    response = msg
                    break

        assert response is not None, "Did not receive LOGENESIS_RESPONSE"
        assert response["state"] == "AWAKENED"
        assert response["visual_qualia"]["shape"] == "shard"
        print(f"Test 1 Passed: {response['text_content']}")

        # Test 2: Emotion
        # Send multiple times to overcome state inertia/drift
        payload["input"]["text"] = "I feel so sad and tired"
        payload["input"]["session_id"] = "emotion_test_session"

        last_response = None
        # Send 3 times to drift state towards purple threshold
        for _ in range(3):
            websocket.send_text(json.dumps(payload))
            # Consume response for each send
            for _ in range(5):
                data = websocket.receive_text()
                msg = json.loads(data)
                if msg.get("type") == "LOGENESIS_RESPONSE":
                    last_response = msg
                    break

        assert last_response is not None
        # Color drifts from #e0e0e0 towards #A855F7.
        # After 3 steps it reaches approx #c6a0ea
        assert last_response["visual_qualia"]["color"] != "#e0e0e0"
        assert last_response["visual_qualia"]["color"] == "#c6a0ea" or last_response["visual_qualia"]["color"] == "#A855F7"
        print(f"Test 2 Passed: {last_response['text_content']}")

        # Test 3: Nirodha
        payload["input"]["text"] = "time to sleep now"
        websocket.send_text(json.dumps(payload))

        response = None
        for _ in range(10):
            data = websocket.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "LOGENESIS_RESPONSE":
                response = msg
                break

        assert response is not None
        assert response["state"] == "NIRODHA"
        assert response["visual_qualia"]["color"] == "#050505"
        print(f"Test 3 Passed: {response['text_content']}")

if __name__ == "__main__":
    test_logenesis_flow()
