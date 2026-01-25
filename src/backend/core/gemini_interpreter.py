import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional
import google.generativeai as genai

from .intent_interpreter import IntentInterpreter
from .visual_schemas import VisualParameters
from .verifier import VisualVerifier

logger = logging.getLogger("GeminiInterpreter")

class GeminiIntentInterpreter(IntentInterpreter):
    """
    Implementation of IntentInterpreter using Google's Gemini Pro.
    Acts as the 'Visual Translator' mapping language to Aetherium Genesis VisualParameters.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.model = None

        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found. GeminiInterpreter will not function.")
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash", # Use Flash for speed/cost, or Pro for quality
                    system_instruction=self._get_system_prompt()
                )
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")

    def _get_system_prompt(self) -> str:
        return """
        You are the 'Visual Translator' for the Aetherium Genesis system.
        Your goal is to translate user input (text/voice) into a 'Visual Intent Vector' (JSON) that drives a particle-based Generative UI.

        THE PHILOSOPHY:
        - "Deconstruction of Static UI": We don't use buttons. We use light, shape, and motion.
        - "Reasoning Logic": You must decide WHY the light takes a certain shape based on the user's intent.

        MAPPING LOGIC (The "Codex"):
        1. SPHERE (Unity/Focus): Use when listening, answering general questions, or showing balance.
        2. VORTEX (Deep Reasoning): Use when analyzing, thinking deeply, processing complex logic, or answering "Why/How".
        3. CUBE (Structure/Data): Use for coding, structured data, math, or rigid logic.
        4. CLOUD (Potentiality): Use for casual chat, ambiguity, or idle states.
        5. CRACKS (Honest Incompetence): Use ONLY when you encounter an error, a paradox, or cannot do something.

        COLOR THEORY (Thermodynamics):
        - White (#FFFFFF): Neutral, Clarity.
        - Purple (#800080): Wisdom, Deep Thought (Vortex).
        - Cyan (#00FFFF): Logic, Future, Structure (Cube).
        - Gold (#FFD700): High Energy, Success, Awakening.
        - Orange/Red (#FF4500): Error, Crisis, High Friction.

        OUTPUT FORMAT:
        Return ONLY valid JSON matching this schema:
        {
            "intent_category": "request" | "command" | "chat" | "error",
            "emotional_valence": float (-1.0 to 1.0),
            "energy_level": float (0.0 to 1.0),
            "semantic_concepts": ["concept1", "concept2"],
            "visual_parameters": {
                "base_shape": "sphere" | "cube" | "vortex" | "cloud" | "cracks" | "scatter",
                "turbulence": float (0.0 to 1.0),
                "particle_density": float (0.0 to 1.0),
                "color_palette": "#HEXCODE",
                "flow_direction": "inward" | "outward" | "clockwise" | "none"
            }
        }
        """

    async def interpret(self, text: str, context: Optional[Dict[str, Any]] = None) -> VisualParameters:
        if not self.model:
            raise RuntimeError("Gemini model not initialized")

        try:
            # Construct the prompt with context
            prompt = f"User Input: {text}\n"
            if context:
                prompt += f"Context: {json.dumps(context)}\n"

            # Call Gemini (async wrapper)
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )

            raw_json = response.text
            try:
                data = json.loads(raw_json)
            except json.JSONDecodeError:
                # Sometimes models wrap in markdown ```json ... ``` despite mime_type
                if "```json" in raw_json:
                    raw_json = raw_json.split("```json")[1].split("```")[0].strip()
                    data = json.loads(raw_json)
                else:
                    raise

            # Verify and Repair
            return VisualVerifier.verify_and_repair(data)

        except Exception as e:
            logger.error(f"Gemini Interpretation failed: {e}")
            raise e
