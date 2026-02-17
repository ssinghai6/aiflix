from typing import Dict, Any
from .base_agent import BaseAgent
from ..llm import get_llm
from ..rag.retriever import KnowledgeRetriever
from ..rag.templates import CINEMATOGRAPHY_SYSTEM_PROMPT
from ..utils import safe_json_parse, logger
import json

class DOPAgent(BaseAgent):
    def __init__(self, provider: str = "mock"):
        super().__init__(name="DOPAgent")
        self.llm = get_llm(provider)
        self.retriever = KnowledgeRetriever()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        script_data = input_data.get("script_data", {})
        feedback = input_data.get("feedback", "")        
        identities = input_data.get("identities", []) # List of IdentityProfile dicts
        
        logger.info(f"{self.name} analyzing script for visual translation...")

        # 1. Retrieve RAG Context
        knowledge_items = self.retriever.retrieve("lighting camera angle cinematic", category="Cinematography")
        context_str = self.retriever.format_context(knowledge_items)

        # Inject Identity Context
        identity_context = ""
        if identities:
           identity_context = "\n### Identity Constraints (MUST USE VISUAL EMBEDDING TRIGGERS):\n"
           for profile in identities:
               identity_context += f"- {profile['name']}: Trigger='{profile['visual_embedding_trigger']}', Appearance='{profile['canonical_appearance']}'\n"
        
        context_str += identity_context

        # 2. Construct Prompt
        system_prompt = CINEMATOGRAPHY_SYSTEM_PROMPT.format(context=context_str)
        user_prompt = f"Generate optical specifications for this script:\n{json.dumps(script_data)}"
        
        if feedback:
            user_prompt += f"\n\nIMPORTANT FEEDBACK FROM CRITIC: {feedback}"

        # 3. Call LLM
        response = self.llm.generate(user_prompt, system_prompt=system_prompt)
        
        # 4. Parse and Return
        shot_list_data = safe_json_parse(response)
        return shot_list_data
