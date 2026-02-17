from pathlib import Path
import os
import requests
import time
from ..config import Config
from ..utils import logger

class HuggingFaceVideoGenerator:
    """
    Wrapper for Hugging Face Inference API.
    NOTE: Free tier support for Image-to-Video (SVD) is spotty. 
    Falling back to Text-to-Video (damo-vilab) for reliable free generation if SVD fails.
    """
    
    def __init__(self, model_name: str = "damo-vilab/text-to-video-ms-1.7b"):
        # Alternative: "ali-vilab/modelscope-damo-text-to-video-synthesis"
        self.model_name = model_name
        self.api_url = f"https://router.huggingface.co/hf-inference/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {Config.HF_TOKEN}"}
        
    def generate(self, image_path: Path, prompt: str, output_path: Path) -> Path:
        """
        Generates video via Hugging Face Inference API.
        Note: Ignores image_path for Text-to-Video models.
        """
        if not Config.HF_TOKEN:
            logger.error("HF_TOKEN not found. Skipping video generation.")
            return None
            
        logger.info(f"Generating video with {self.model_name}...")
        
        try:
            # Text-to-Video Payload
            payload = {"inputs": prompt}
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                logger.error(f"HF API Error: {response.text}")
                return None
            
            # Response should be MP4 bytes
            if "video" in response.headers.get("content-type", "") or response.headers.get("content-type") == "application/octet-stream":
                 video_bytes = response.content
            else:
                 logger.warning(f"Unexpected response type: {response.headers.get('content-type')}")
                 return None

            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(video_bytes)
            logger.info(f"Video saved to {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Hugging Face video generation failed: {e}")
            return None
