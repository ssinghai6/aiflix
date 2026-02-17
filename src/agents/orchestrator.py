from typing import Dict, Any
from .screenwriter import ScreenplayAgent
from .dop import DOPAgent
from .critic import CriticAgent
from .identity import IdentityManager
from ..media.engine import VisualEngine
from ..state import ProjectState
from ..utils import logger
from ..config import Config

class Orchestrator:
    """
    The 'Digital Studio Head' that manages the distributed cinematic intelligence.
    Enforces the workflow: Concept -> Identity -> Narrative -> Visual Planning -> Critique -> Production.
    """
    def __init__(self, llm_provider: str = "mock"):
        self.state = None
        
        # The Crew
        self.screenwriter = ScreenplayAgent(provider=llm_provider)
        self.dop = DOPAgent(provider=llm_provider)
        self.critic = CriticAgent(provider=llm_provider)
        self.identity_manager = IdentityManager(provider=llm_provider)
        
        # The Production Engine
        self.visual_engine = VisualEngine()
    
    def run_pipeline(self, concept: str, max_shots: int = None) -> Dict[str, Any]:
        logger.info(f"*** STUDIO HEAD INITIALIZED FOR: {concept} ***")
        
        # 0. Initialize State
        self.state = ProjectState(title="Untitled", logline=concept, genre="Unknown")
        self.state.log_event("StudioHead", "greenlight_project", concept)
        
        # 1. Identity Phase (Whose story is this?)
        logger.info("--- Phase 1: Identity Definition ---")
        identity_data = self.identity_manager.run({"concept": concept})
        self.state.log_event("IdentityManager", "profiles_generated")
        
        if identity_data and "profiles" in identity_data:
            self.identity_manager.update_state(self.state, identity_data)
            logger.info(f"Identities locked: {list(self.state.identities.keys())}")
        else:
            logger.warning("Identity generation returned incomplete data.")
        
        # 2. Information Handover: Identity -> Screenwriter
        # Update: We now pass the identity context implicitly or explicitly if needed.
        # The screenwriter primarily needs concept, but knowing characters helps.
        
        # 3. Narrative Phase (The Script)
        logger.info("--- Phase 2: Narrative Engineering ---")
        script_input = {
            "concept": concept,
            "identities": [p.__dict__ for p in self.state.identities.values()]
        }
        script_data = self.screenwriter.run(script_input)
        
        if not script_data:
            logger.error("Screenwriting failed. Aborting.")
            return {}
            
        self.state.title = script_data.get("title", "Untitled")
        logger.info(f"Script Locked: {self.state.title}")
        
        # 4. Visualization Phase (The Shot List)
        logger.info("--- Phase 3: Cinematography & Critique ---")
        
        shot_list_data = {}
        feedback = ""
        max_retries = 3
        
        for i in range(max_retries):
            logger.info(f"Optimization Loop {i+1}/{max_retries}...")
            
            # DOP input includes Script AND Identity Constraints
            dop_input = {
                "script_data": script_data,
                "identities": [p.__dict__ for p in self.state.identities.values()]
            }
            if feedback:
                dop_input["feedback"] = feedback
                
            shot_list_data = self.dop.run(dop_input)
            
            # Critic evaluates
            critique = self.critic.run({
                "script_data": script_data,
                "shot_list_data": shot_list_data
            })
            
            if critique.get("status") == "approved":
                logger.info("Critic APPROVED the visual plan.")
                break
            else:
                feedback = critique.get("feedback", "Improve visual prompts.")
                logger.info(f"Critic REJECTED. Feedback: {feedback}")
        
        if not shot_list_data:
            logger.error("DOP planning failed.")
            return {"script": script_data}
            
        # --- SAVE ARTIFACTS FOR USER VISIBILITY ---
        import json
        output_path = Config.OUTPUT_DIR
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save Screenplay
        with open(output_path / "screenplay.json", "w") as f:
            json.dump(script_data, f, indent=2)
        
        # Save Shotlist
        with open(output_path / "shotlist.json", "w") as f:
            json.dump(shot_list_data, f, indent=2)
            
        logger.info(f"💾 Screenplay & Shotlist saved to {output_path}")
        # -------------------------------------------
            
        # 5. Production Phase (Visual Engine)
        logger.info("--- Phase 4: Production (Anchor-First Execution) ---")
        produced_shots = []
        
        shots_to_produce = shot_list_data.get("shots", [])
        if max_shots:
            logger.info(f"Limiting production to first {max_shots} shots.")
            shots_to_produce = shots_to_produce[:max_shots]
            
        for shot in shots_to_produce:
            result = self.visual_engine.generate_shot(shot)
            if result["status"] == "success":
                produced_shots.append(result)
                self.state.log_event("VisualEngine", "shot_produced", str(shot.get("shot_id", "unknown")))
            else:
                logger.error(f"Failed to produce shot {shot.get('shot_id')}")
        
        logger.info(f"Production Wrap. {len(produced_shots)} shots completed.")
        
        return {
            "state": self.state,
            "script": script_data,
            "shot_list": shot_list_data,
            "produced_content": produced_shots
        }
