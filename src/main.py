import argparse
import sys
import os
from pathlib import Path

# Add project root to python path to ensure imports work
sys.path.append(os.getcwd())

from src.agents.orchestrator import Orchestrator
from src.config import Config
from src.utils import logger

def main():
    parser = argparse.ArgumentParser(description="AiFlix: Distributed Cinematic Intelligence Studio")
    parser.add_argument("concept", type=str, help="The high-level concept or logline for the movie.")
    parser.add_argument("--max_shots", type=int, default=None, help="Limit the number of shots produced (default: unlimited).")
    parser.add_argument("--api", action="store_true", help="Start as a FastAPI server (Coming Soon).")
    
    args = parser.parse_args()
    
    if args.api:
        logger.info("Starting API Server... (Not implemented yet, check PRODUCTION.md)")
        return

    logger.info(f"🎬 Starting Studio Production for: '{args.concept}'")
    
    # Initialize Studio Head
    orchestrator = Orchestrator(llm_provider="groq")
    
    # Run Pipeline
    try:
        result = orchestrator.run_pipeline(args.concept, max_shots=args.max_shots)
        
        if result:
            script_title = result.get("script", {}).get("title", "Untitled")
            shot_count = len(result.get("produced_content", []))
            print(f"\n✅ Production Complete!")
            print(f"   Title: {script_title}")
            print(f"   Shots Produced: {shot_count}")
            print(f"   Output Directory: {Config.OUTPUT_DIR}/shots")
        else:
            print("\n❌ Production Failed.")
            
    except Exception as e:
        logger.error(f"Critical error during production: {e}")
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
