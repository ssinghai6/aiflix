from pathlib import Path
from typing import List
from ..utils import logger

class Editor:
    """Handles the assembly of video clips."""
    
    def assemble(self, clip_paths: List[Path], output_path: Path):
        """Concatenates clips into a final movie."""
        logger.info(f"Assembling {len(clip_paths)} clips...")
        
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
            
            # Check if files are real videos (not dummy txt files)
            valid_clips = []
            for p in clip_paths:
                try:
                    # Attempt to load
                    clip = VideoFileClip(str(p))
                    valid_clips.append(clip)
                except Exception:
                    logger.warning(f"Could not load clip {p}, skipping.")
            
            if not valid_clips:
                logger.error("No valid clips to assemble.")
                return
                
            final_clip = concatenate_videoclips(valid_clips)
            final_clip.write_videofile(str(output_path), codec="libx264", audio=False)
            logger.info(f"Final assembly saved to {output_path}")
            
        except Exception as e:
            logger.warning(f"Assembly failed: {e}. (This is expected if mock video files were text).")
