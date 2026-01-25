from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .visual_schemas import VisualParameters

class IntentInterpreter(ABC):
    """
    Abstract Base Class for interpreting natural language into VisualParameters.
    Follows the 'Visual Translator' role described in Aetherium Genesis.
    """

    @abstractmethod
    async def interpret(self, text: str, context: Optional[Dict[str, Any]] = None) -> VisualParameters:
        """
        Translates the user's text (and optional context) into a VisualParameters object.
        """
        pass
