from pathlib import Path
import os
import requests
import time
from ..config import Config
from ..utils import logger

class HuggingFaceImageGenerator:
    """Wrapper for Hugging Face Inference API Image Generation (FLUX.1-schnell)."""
    
    def __init__(self, model_name: str = "black-forest-labs/FLUX.1-schnell"):
        self.model_name = model_name
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {Config.HF_TOKEN}"}
        
    def generate(self, prompt: str, output_path: Path, aspect_ratio: str = "16:9") -> Path:
        """
        Generates an image via Hugging Face Inference API.
        """
        if not Config.HF_TOKEN:
            logger.error("HF_TOKEN not found. Skipping image generation.")
            return None
            
        logger.info(f"Generating image with {self.model_name}: {prompt[:50]}...")
        
        # Add aspect ratio instruction to prompt since HF API is raw
        enhanced_prompt = f"{prompt} --aspect_ratio {aspect_ratio}"
        
        payload = {
            "inputs": enhanced_prompt,
            "parameters": {
                "num_inference_steps": 4, # Schnell is fast
                "guidance_scale": 0.0, # Schnell uses 0 guidance usually or low
                "width": 1024,
                "height": 576 if aspect_ratio == "16:9" else 1024
            }
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                logger.error(f"HF API Error: {response.text}")
                return None
            
            # HF returns raw bytes for image usually
            if response.headers.get("content-type") == "image/jpeg" or response.headers.get("content-type") == "image/png":
                 image_bytes = response.content
            else:
                 # Sometimes it returns a loading status if model is cold
                 logger.warning(f"Unexpected response type: {response.headers.get('content-type')}")
                 return None

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            logger.info(f"Image saved to {output_path}")
            return output_path
                
        except Exception as e:
            logger.error(f"Hugging Face generation failed: {e}")
            return None
