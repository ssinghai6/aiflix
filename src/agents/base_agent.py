from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAgent(ABC):
    """Abstract base class for all AiFlix agents."""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the agent's main logic."""
        pass
