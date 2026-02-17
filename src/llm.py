from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import time
from .config import Config
from .utils import logger

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        """Generates text from the LLM."""
        pass

class MockLLM(LLMProvider):
    """A mock LLM for testing workflows without API costs or GPU requirements."""
    
    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        logger.info(f"MockLLM generating response for prompt: {prompt[:50]}...")
        # Simulate latency
        time.sleep(0.5)
        
        prompt_lower = prompt.lower()
        
        if "define visual profiles" in prompt_lower:
            return '''
            {
                "profiles": [
                    {
                        "name": "Detective Cole",
                        "archetype": "The Anti-Hero",
                        "visual_embedding_trigger": "img_ch_cole",
                        "canonical_appearance": "40s, weary face, stubble, trench coat, glowing blue cybernetic scope on left eye.",
                        "wardrobe": {
                            "default": "Weathered leather trench coat over tactical vest.",
                            "formal": "N/A"
                        }
                    }
                ]
            }
            '''
        
        elif "develop the narrative" in prompt_lower:
            return '''
            {
                "scene_header": {
                    "slugline": "EXT. NEON ALLEY - NIGHT",
                    "focal_character": "Detective Cole"
                },
                "act_structure": {
                    "act": "I",
                    "beat": "Inciting Incident"
                },
                "character_arcs": {
                    "Detective Cole": "Apathetic -> Curious"
                },
                "scene_beats": [
                    {
                        "action": "Rain slicks the pavement. COLE (40s) lights a cigarette, illuminating his cybernetic eye.",
                        "dialogue": "COLE: Another glitch in the matrix.",
                        "emotional_shift": "Resignation"
                    },
                    {
                        "action": "He spots a GLOWING ARTIFACT in the trash.",
                        "dialogue": "",
                        "emotional_shift": "Intrigue"
                    }
                ],
                "emotional_trajectory": ["Weary", "Alert"],
                "visual_intent_markers": ["High Contrast", "Noir", "Neon"]
            }
            '''
            
        elif "generate optical specifications" in prompt_lower:
            return '''
            {
                "shots": [
                    {
                        "shot_id": 1,
                        "narrative_beat_ref": "Cole lights cigarette",
                        "shot_type": "medium_close_up",
                        "lens_mm": 50,
                        "lighting": {
                            "key": "soft_neon_blue",
                            "fill": "negative",
                            "ratio": "8:1"
                        },
                        "movement": {
                            "type": "static",
                            "speed": "N/A"
                        },
                        "aspect_ratio": "2.39:1",
                        "mood": "tech_noir",
                        "visual_prompt": "img_ch_cole, medium close up, lighting cigarette, neon rain background, cybernetic eye glow, 50mm lens, cinematic lighting"
                    },
                    {
                        "shot_id": 2,
                        "narrative_beat_ref": "Spots artifact",
                        "shot_type": "close_up",
                        "lens_mm": 85,
                        "lighting": {
                            "key": "artifact_glow_gold",
                            "fill": "dim_street",
                            "ratio": "4:1"
                        },
                        "movement": {
                            "type": "dolly_in",
                            "speed": "slow"
                        },
                            "aspect_ratio": "2.39:1",
                        "mood": "mystery",
                        "visual_prompt": "close up of glowing golden artifact in trash, wet pavement, shallow depth of field, 85mm lens"
                    }
                ]
            }
            '''
        
        elif "evaluate this shot list" in prompt_lower:
            return '''
            {
                "status": "approved",
                "feedback": "Visuals align well with narrative."
            }
            '''

        else:
            # Default generic fallback or pass through for other tests
            return '{"error": "MockLLM could not match prompt pattern."}'

class OpenAILLM(LLMProvider):
    """Wrapper for OpenAI API."""
    
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.api_key = Config.OPENAI_API_KEY
        # Lazy import to avoid hard dependency if not used
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            logger.warning("OpenAI library not installed. OpenAILLM will not work.")
            self.client = None

    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        if not self.client:
            return "Error: OpenAI client not initialized."
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return ""

class GroqLLM(LLMProvider):
    """Wrapper for Groq API."""
    
    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.api_key = Config.GROQ_API_KEY
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            logger.warning("Groq library not installed. GroqLLM will not work.")
            self.client = None

    def generate(self, prompt: str, system_prompt: str = "", **kwargs) -> str:
        if not self.client:
            return "Error: Groq client not initialized."
            
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API call failed: {e}")
            return ""

def get_llm(provider_name: str = "groq") -> LLMProvider:
    """Factory function to get LLM provider."""
    if provider_name.lower() == "openai":
        return OpenAILLM()
    elif provider_name.lower() == "groq":
        return GroqLLM()
    return MockLLM()
