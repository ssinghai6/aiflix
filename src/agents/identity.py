from typing import Dict, Any, List
from .base_agent import BaseAgent
from ..llm import get_llm
from ..state import ProjectState, IdentityProfile
from ..utils import safe_json_parse, logger
import json

IDENTITY_SYSTEM_PROMPT = """
You are the Identity Manager for a cinematic production.
Your goal is to define canonical visual profiles for characters to ensure consistency across the movie.

Output must be a JSON object:
{
    "profiles": [
        {
            "name": "Character Name",
            "archetype": "The Hero / The Villain",
            "visual_embedding_trigger": "unique_trigger_word",
            "canonical_appearance": "Detailed physical description (face, body, age, key features).",
            "wardrobe": {
                "default": "Primary outfit description",
                "alternate": "Secondary outfit"
            }
        }
    ]
}
"""

class IdentityManager(BaseAgent):
    def __init__(self, provider: str = "mock"):
        super().__init__(name="IdentityManager")
        self.llm = get_llm(provider)

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes the script or concept to extract characters and define their visual profiles.
        """
        concept = input_data.get("concept", "")
        script_data = input_data.get("script_data", {})
        
        logger.info(f"{self.name} defining character identities...")
        
        context = f"Concept: {concept}\n"
        if script_data:
            context += f"Characters in script: {script_data.get('characters', [])}"

        response = self.llm.generate(
            prompt=f"Define visual profiles for the main characters in this context:\n{context}",
            system_prompt=IDENTITY_SYSTEM_PROMPT
        )
        
        result = safe_json_parse(response)
        return result

    def update_state(self, state: ProjectState, profiles_data: Dict[str, Any]):
        """Updates the global project state with new identities."""
        for p_data in profiles_data.get("profiles", []):
            profile = IdentityProfile(**p_data)
            state.register_identity(profile)
