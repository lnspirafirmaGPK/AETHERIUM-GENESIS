from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import logging
import asyncio
from typing import List

# Adjust imports based on execution context (running from repo root)
try:
    from src.backend.core.lcl import LightControlLogic
    from src.backend.core.lightweight_ai import LightweightAI
    from src.backend.core.ai_adapter import MockAdapter
    from src.backend.core.google_search_provider import GoogleSearchProvider
    from src.backend.core.search_schemas import SearchIntent
    from src.backend.core.light_schemas import LightIntent, LightAction
except ImportError:
    # Fallback for local testing if paths differ
    from core.lcl import LightControlLogic
    from core.lightweight_ai import LightweightAI
    from core.ai_adapter import MockAdapter
    from core.google_search_provider import GoogleSearchProvider
    from core.search_schemas import SearchIntent
    from core.light_schemas import LightIntent, LightAction

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
search_provider = GoogleSearchProvider()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("Client connected to Light Interaction Testbed")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info("Client disconnected")

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                # Handle disconnected clients gracefully if logic fails
                logger.warning(f"Broadcast error: {e}")

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(physics_loop())

async def physics_loop():
    logger.info("Starting Physics Loop")
    while True:
        try:
            state = lcl.tick(0.05) # 20Hz -> 0.05s

            # Wrap in a message type for frontend differentiation
            # We construct manual JSON to wrap the Pydantic output
            state_json = state.model_dump_json()
            msg = f'{{"type": "STATE", "data": {state_json}}}'

            await manager.broadcast(msg)
        except Exception as e:
            logger.error(f"Physics Loop Error: {e}")

        await asyncio.sleep(0.05)

@app.get("/")
async def root():
    return {"status": "Aetherium Genesis Backend Online", "modules": ["LCL", "LightweightAI", "MockAdapter"]}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

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

            if intent:
                if isinstance(intent, SearchIntent):
                    # Perform Search
                    logger.info(f"Executing Search: {intent.query}")
                    results = search_provider.search(intent.query)

                    # Synthesize LightIntent based on results
                    summary = "No results found."
                    color_hint = "purple"
                    intensity = 0.3

                    if results:
                        first_result = results[0]
                        title = first_result.get("title", "")
                        snippet = first_result.get("snippet", "")
                        summary = f"{title}: {snippet}"
                        color_hint = "white"
                        intensity = 0.8

                    # Create synthesized intent
                    light_intent = LightIntent(
                        action=LightAction.EMPHASIZE,
                        target="GLOBAL",
                        intensity=intensity,
                        color_hint=color_hint,
                        source="search_provider"
                    )

                    # Process via LCL
                    instruction = lcl.process(light_intent)
                    if instruction:
                        instruction.text_content = summary
                        await websocket.send_text(instruction.model_dump_json())

                else:
                    # Set source metadata
                    intent.source = "ai" if mode == "ai" else user_input.get("type", "unknown")

                    # Pass through Light Control Logic (LCL)
                    instruction = lcl.process(intent)
                    logger.info(f"LCL Generated Instruction: {instruction}")

                    if instruction:
                        # Send Instruction to Client
                        await websocket.send_text(instruction.model_dump_json())
            else:
                logger.warning("No intent resolved")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Internal Error: {e}")
        manager.disconnect(websocket)
