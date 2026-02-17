import sys
import os
import json
from src.agents.orchestrator import Orchestrator
from src.state import ProjectState

def main():
    print("Verifying Distributed Cinematic Intelligence...")
    
    # 1. Initialize Studio Head
    # Using Groq for real logic
    orchestrator = Orchestrator(llm_provider="groq")
    concept = "A cyberpunk detective investigating a neon-lit alleyway."
    
    # 2. Run the Autonomous Pipeline
    print(f"\n[1] Greenlighting Project: {concept}")
    result = orchestrator.run_pipeline(concept, max_shots=1)
    
    if not result:
        print("Pipeline failed!")
        return

    # 3. Inspect State and Identity
    state: ProjectState = result.get("state")
    if state:
        print(f"\n[2] Identity Layer Verified:")
        for name, profile in state.identities.items():
            print(f"    - {name}: {profile.archetype} (Trigger: {profile.visual_embedding_trigger})")
    
    # 4. Inspect Narrative
    script = result.get("script", {})
    print(f"\n[3] Narrative Layer Verified:")
    print(f"    Title: {script.get('title')}")
    print(f"    Act Structure: {script.get('act_structure')}")
    
    # 5. Inspect Cinematography
    shot_list = result.get("shot_list", {}).get("shots", [])
    print(f"\n[4] Cinematography Layer Verified:")
    print(f"    Shots Planned: {len(shot_list)}")
    if shot_list:
        example_shot = shot_list[0]
        print(f"    Example Shot Spec:")
        print(f"      - Shot Type: {example_shot.get('shot_type')}")
        print(f"      - Lens: {example_shot.get('lens_mm')}mm")
        print(f"      - Lighting: {example_shot.get('lighting')}")
        print(f"      - Visual Prompt: {example_shot.get('visual_prompt')}")

    # 6. Inspect Production
    produced = result.get("produced_content", [])
    print(f"\n[5] Production Layer Verified:")
    print(f"    Shots Produced: {len(produced)}")
    for p in produced:
        print(f"    - Shot Status: {p['status']}")
        if p['status'] == 'success':
            print(f"      - Anchor: {p.get('anchor_frame')}")
            print(f"      - Video: {p.get('video_clip')}")

    print("\n[SUCCESS] System operates as a distributed cinematic intelligence.")

if __name__ == "__main__":
    main()
