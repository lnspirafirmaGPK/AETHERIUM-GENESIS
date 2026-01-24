from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging

# Adjust imports based on execution context (running from repo root)
try:
    from src.backend.core.lcl import LightControlLogic
    from src.backend.core.lightweight_ai import LightweightAI
    from src.backend.core.ai_adapter import MockAdapter
except ImportError:
    # Fallback for local testing if paths differ
    from core.lcl import LightControlLogic
    from core.lightweight_ai import LightweightAI
    from core.ai_adapter import MockAdapter

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("LightTestbed")

app = FastAPI(title="Aetherium Genesis - Light Testbed")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Components
lcl = LightControlLogic()
lightweight_ai = LightweightAI()
mock_adapter = MockAdapter()

@app.get("/")
async def root():
    return {"status": "Aetherium Genesis Backend Online", "modules": ["LCL", "LightweightAI", "MockAdapter"]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected to Light Interaction Testbed")

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")

            try:
                message = json.loads(data)
            except json.JSONDecodeError:
                error_msg = {"error": "Invalid JSON format"}
                await websocket.send_text(json.dumps(error_msg))
                continue

            # Protocol: { "mode": "std" | "ai", "input": { ... } }
            mode = message.get("mode", "std")
            user_input = message.get("input", {})

            intent = None

            if mode == "ai":
                # AI Adapter Path
                # Input expected to contain "text" for the prompt
                prompt = user_input.get("text", "")
                # Scene state is empty for now
                intent = await mock_adapter.generate_intent(prompt, {})
                logger.info(f"AI Adapter Generated Intent: {intent}")
            else:
                # Lightweight AI Core Path (Rule-based)
                # Handles "touch", "voice" regex
                intent = lightweight_ai.resolve_intent(user_input)
                logger.info(f"Lightweight Core Resolved Intent: {intent}")

            # Pass through Light Control Logic (LCL)
            instruction = lcl.process(intent)
            logger.info(f"LCL Generated Instruction: {instruction}")

            # Send Instruction to Client
            await websocket.send_text(instruction.model_dump_json())

    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Internal Error: {e}")
        await websocket.close()
