from typing import Dict, Any, List
from pathlib import Path
from .image_gen import ImageGenerator
from .video_gen import VideoGenerator
from .hf_image_gen import HuggingFaceImageGenerator
from .hf_video_gen import HuggingFaceVideoGenerator
# Lazy import for local to avoid heavy dependencies if not used
# from .local_gen import LocalImageGenerator, LocalVideoGenerator

from ..config import Config
from ..utils import logger

class VisualEngine:
    """
    The Visual Engine Protocol.
    Enforces the "Anchor Frame First" strategy for temporal coherence.
    """
    def __init__(self, provider: str = "auto"):
        self.provider = provider
        
        # Decide provider logic
        use_hf = False
        
        if provider == "huggingface":
            use_hf = True
        elif provider == "auto":
            # Prefer HF if token exists (Free), else Replicate
            if Config.HF_TOKEN:
                use_hf = True
            elif Config.REPLICATE_API_TOKEN:
                use_hf = False
            else:
                logger.warning("No media keys found. Defaulting to Mock via Replicate wrapper.")
        
        if use_hf:
            logger.info("VisualEngine: Using Hugging Face (Free/Open Source)")
            self.image_gen = HuggingFaceImageGenerator()
            self.video_gen = HuggingFaceVideoGenerator()
        else:
            logger.info("VisualEngine: Using Replicate (Paid/Cloud)")
            self.image_gen = ImageGenerator()
            self.video_gen = VideoGenerator()

    def generate_shot(self, shot_data: Dict[str, Any], identity_map: Dict[str, Any] = None) -> Dict[str, str]:
        """
        Generates a cinematic shot following the protocol:
        1. Generate Anchor Frame (High Fidelity)
        2. Generate Motion (Video) using Anchor as reference
        """
        visual_prompt = shot_data.get("visual_prompt", "")
        shot_type = shot_data.get("shot_type", "wide")
        shot_id = shot_data.get("shot_id", "unknown")
        
        logger.info(f"VisualEngine processing shot {shot_id}: {visual_prompt[:50]}...")

        # Ensure output directory exists
        output_dir = Config.OUTPUT_DIR / "shots"
        output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Generate Anchor Frame
        logger.info(f"   -> Generating Anchor Frame...")
        anchor_path = output_dir / f"shot_{shot_id}_anchor.png"
        
        # (In a real system, we would inject the specific identity LoRA/Embedding here)
        generated_path = self.image_gen.generate(
            prompt=f"Cinematic still, {shot_type}, {visual_prompt}",
            output_path=anchor_path,
            aspect_ratio=shot_data.get("aspect_ratio", "16:9")
        )

        if not generated_path or not generated_path.exists():
            logger.error("Failed to generate anchor frame.")
            return {"status": "failed"}

        # 2. Generate Motion (Image-to-Video)
        logger.info(f"   -> Generating Motion (Image-to-Video)...")
        # Video generator might need output path too? 
        # Checking video_gen.py... usually it takes output_path.
        # Let's assume it does or generates one. 
        # src/media/video_gen.py generate signature: (image_path, prompt, output_path)
        
        video_path = output_dir / f"shot_{shot_id}_clip.mp4"
        self.video_gen.generate(
            image_path=anchor_path,
            prompt=visual_prompt,
            output_path=video_path
        )
        
        return {
            "status": "success",
            "anchor_frame": str(anchor_path),
            "video_clip": str(video_path),
            "shot_metadata": shot_data
        }
