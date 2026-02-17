from pathlib import Path
import replicate
import requests
from ..config import Config
from ..utils import logger

class ImageGenerator:
    """Wrapper for FLUX.1 Image Generation via Replicate."""
    
    def __init__(self, model_name: str = "black-forest-labs/flux-dev"):
        self.model_name = model_name
        
    def generate(self, prompt: str, output_path: Path, aspect_ratio: str = "16:9") -> Path:
        """
        Generates an image via Replicate API.
        """
        if not Config.REPLICATE_API_TOKEN:
            logger.error("REPLICATE_API_TOKEN not found. Skipping image generation.")
            return None
            
        logger.info(f"Generating image with {self.model_name}: {prompt[:50]}...")
        
        try:
            output = replicate.run(
                self.model_name,
                input={
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                    "output_quality": 90
                }
            )
            
            # Replicate returns a list of output URLs for Flux
            image_url = output[0] if isinstance(output, list) else output
            
            # Download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(response.content)
                logger.info(f"Image saved to {output_path}")
                return output_path
            else:
                logger.error(f"Failed to download image from {image_url}")
                return None
                
        except Exception as e:
            logger.error(f"Replicate generation failed: {e}")
            return None
