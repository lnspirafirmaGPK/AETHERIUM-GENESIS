from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .visual_schemas import EmbodimentContract

class IntentInterpreter(ABC):
    """
    Abstract Base Class for interpreting natural language into EmbodimentContract.
    Follows the 'Visual Translator' role described in Aetherium Genesis.
    """

    @abstractmethod
    async def interpret(self, text: str, context: Optional[Dict[str, Any]] = None) -> EmbodimentContract:
        """
        Translates the user's text (and optional context) into an EmbodimentContract object.
        """
        pass
