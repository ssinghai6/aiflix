import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
try:
    from diffusers import TextToVideoSDPipeline
except ImportError:
    print("TextToVideoSDPipeline not found in diffusers!")
    exit(1)

def test_local():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Device: {device}")
    
    # Check Image Gen
    print("Loading SDXL-Turbo...")
    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/sdxl-turbo", 
        torch_dtype=torch.float16 if device == "mps" else torch.float32, 
        variant="fp16" if device == "mps" else None
    )
    pipe.to(device)
    
    # FIX: Force VAE to float32 to avoid gray noise artifacts on Mac
    if device == "mps":
        pipe.vae.to(dtype=torch.float32)
        
    print("Generating Image...")
    pipe(prompt="A cinematic shot of a cyberpunk city, neon lights, rain, 8k", num_inference_steps=4, guidance_scale=0.0).images[0].save("test_local_image_fixed.png")
    print("Image Saved to test_local_image_fixed.png")
    
    # Check Video Gen
    print("Loading Video Gen...")
    video_pipe = TextToVideoSDPipeline.from_pretrained(
        "damo-vilab/text-to-video-ms-1.7b", 
        torch_dtype=torch.float16 if device == "mps" else torch.float32,
        variant="fp16" if device == "mps" else None
    )
    # video_pipe.enable_model_cpu_offload() # Skip optimization for quick test if possible, or keep it.
    video_pipe.to(device)
    
    print("Generating Video...")
    frames = video_pipe("A cat running", num_frames=8).frames[0]
    export_to_video(frames, "test_local_video.mp4", fps=8)
    print("Video Saved.")

if __name__ == "__main__":
    test_local()
