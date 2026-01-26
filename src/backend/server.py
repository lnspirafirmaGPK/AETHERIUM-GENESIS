import asyncio
import json
import logging
import os
import sys

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from src.backend.core.logenesis_engine import LogenesisEngine
from src.backend.core.logenesis_schemas import LogenesisResponse
from src.backend.core.visual_schemas import TemporalPhase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AetherServer")

app = FastAPI()

# Initialize Engine
engine = LogenesisEngine()

clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    logger.info("Client connected")

    # Session ID for state persistence (simple IP-based or random)
    session_id = str(id(websocket))

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                logger.warning("Invalid JSON received")
                continue

            msg_type = msg.get("type")

            # --- New Protocol (Actuator UI) ---
            if msg_type in ["INTENT_START", "INTENT_END", "INTENT_RECOGNIZED", "RESET"]:

                if msg_type == "INTENT_START":
                    await websocket.send_text(json.dumps({"type": "ACK", "for": "INTENT_START"}))

                elif msg_type == "INTENT_RECOGNIZED":
                    # Text from Client STT
                    text = msg.get("text", "")
                    logger.info(f"Processing Text: {text}")

                    # --- NEW: Immediate Temporal Pulse (Thinking) ---
                    # Send visual feedback BEFORE processing starts to eliminate stutter
                    thinking_params = engine.adapter.get_temporal_visuals(TemporalPhase.THINKING)
                    vp_thinking = thinking_params.model_dump(mode='json')

                    await websocket.send_text(json.dumps({
                        "type": "VISUAL_PARAMS",
                        "params": vp_thinking["visual_parameters"],
                        "meta": {
                            "category": vp_thinking["intent_category"],
                            "valence": vp_thinking["emotional_valence"],
                            "energy": vp_thinking["energy_level"]
                        }
                    }))
                    # -----------------------------------------------

                    response: LogenesisResponse = await engine.process(text, session_id=session_id)

                    # Convert LogenesisResponse to Client Protocol
                    # 1. Visual Params (Check Manifestation Gate)
                    if response.visual_analysis and response.manifestation_granted:
                        # Serialize Pydantic model
                        vp = response.visual_analysis.model_dump(mode='json')
                        # Flat map for the simple UI (or send full object)
                        # The UI expects 'VISUAL_PARAMS' with specific fields.
                        # I'll send the full structure and let UI parse it.
                        await websocket.send_text(json.dumps({
                            "type": "VISUAL_PARAMS",
                            "params": vp["visual_parameters"], # Send the specifics
                            "meta": {
                                "category": vp["intent_category"],
                                "valence": vp["emotional_valence"],
                                "energy": vp["energy_level"]
                            }
                        }))
                    elif response.visual_analysis and not response.manifestation_granted:
                         logger.info("Manifestation Gate: Blocked visual update (Conversational Loop)")

                    # 2. AI Speak
                    if response.text_content:
                        await websocket.send_text(json.dumps({
                            "type": "AI_SPEAK",
                            "text": response.text_content
                        }))

                elif msg_type == "RESET":
                    # Reset Engine State?
                    await websocket.send_text(json.dumps({"type": "ACK", "for": "RESET"}))

            # --- Legacy Protocol (Living Interface PWA) ---
            elif msg.get("mode") == "logenesis":
                # { mode: "logenesis", input: { text: "..." } }
                inp = msg.get("input", {})
                text = inp.get("text", "")

                response: LogenesisResponse = await engine.process(text, session_id=session_id)

                # Send back raw LogenesisResponse (PWA knows how to handle it)
                await websocket.send_text(response.model_dump_json())

    except WebSocketDisconnect:
        clients.discard(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Server Error: {e}")

# Mount static files (Must be after specific routes)
app.mount("/gunui", StaticFiles(directory="gunui"), name="gunui")
app.mount("/", StaticFiles(directory=".", html=True), name="root")
