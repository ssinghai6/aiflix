from typing import Dict, Any
from .base_agent import BaseAgent
from ..llm import get_llm
from ..rag.retriever import KnowledgeRetriever
from ..rag.templates import NARRATIVE_SYSTEM_PROMPT
from ..utils import safe_json_parse, logger

class ScreenplayAgent(BaseAgent):
    def __init__(self, provider: str = "mock"):
        super().__init__(name="ScreenplayAgent")
        self.llm = get_llm(provider)
        self.retriever = KnowledgeRetriever()

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        concept = input_data.get("concept", "")
        logger.info(f"{self.name} processing concept: {concept}")

        # 1. Retrieve RAG Context
        knowledge_items = self.retriever.retrieve(f"{concept} structure hero", category="Screenwriting")
        context_str = self.retriever.format_context(knowledge_items)

        # 2. Construct Prompt
        system_prompt = NARRATIVE_SYSTEM_PROMPT.format(context=context_str)
        user_prompt = f"Develop the narrative for: {concept}"

        # 3. Call LLM
        response = self.llm.generate(user_prompt, system_prompt=system_prompt)
        
        # 4. Parse and Return
        script_data = safe_json_parse(response)
        return script_data
