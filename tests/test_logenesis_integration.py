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
        websocket.send_text(json.dumps(payload))

        response = None
        # Consume messages looking for LOGENESIS_RESPONSE
        for _ in range(10):
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
        payload["input"]["text"] = "I feel so sad and tired"
        websocket.send_text(json.dumps(payload))

        response = None
        for _ in range(10):
            data = websocket.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "LOGENESIS_RESPONSE":
                response = msg
                break

        assert response is not None
        assert response["visual_qualia"]["color"] == "#A855F7" # Purple
        print(f"Test 2 Passed: {response['text_content']}")

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
