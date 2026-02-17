from pathlib import Path
import replicate
import requests
from ..config import Config
from ..utils import logger

class VideoGenerator:
    """Wrapper for CogVideoX via Replicate."""
    
    def __init__(self, model_name: str = "thudm/cogvideox-5b"):
        self.model_name = model_name
        
    def generate(self, image_path: Path, prompt: str, output_path: Path) -> Path:
        """
        Generates video from an anchor image using Replicate.
        """
        if not Config.REPLICATE_API_TOKEN:
            logger.error("REPLICATE_API_TOKEN not found. Skipping video generation.")
            return None
            
        logger.info(f"Generating video with {self.model_name}...")
        
        try:
            # Upload the anchor image temporarily or use open helper if path is local
            # Replicate python client handles path objects usually, but let's be safe
            input_data = {
                "prompt": prompt,
                "image_start": open(image_path, "rb"),
                "num_frames": 49,
                "guidance_scale": 6,
                "num_inference_steps": 50
            }
            
            output = replicate.run(
                self.model_name,
                input=input_data
            )
            
            # Output is typically a URL string for the mp4
            video_url = output
            
            response = requests.get(video_url)
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Video saved to {output_path}")
                return output_path
            else:
                logger.error(f"Failed to download video from {video_url}")
                return None

        except Exception as e:
            logger.error(f"Replicate video generation failed: {e}")
            return None
