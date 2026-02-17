from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from .utils import logger

@dataclass
class IdentityProfile:
    name: str
    archetype: str
    visual_embedding_trigger: str  # e.g., "img_ch_john_doe"
    canonical_appearance: str       # "Late 30s, scar on left cheek..."
    wardrobe: Dict[str, str]        # {"default": "Trench coat", "formal": "Tuxedo"}

@dataclass
class SceneNode:
    scene_id: str
    slugline: str
    time_of_day: str
    location: str
    emotional_beat: str
    narrative_purpose: str
    characters_present: List[str]
    status: str = "pending" # pending, scripted, visualized, filmed

@dataclass
class Event:
    timestamp: str
    agent: str
    action: str
    details: str

@dataclass
class ProjectState:
    """
    The Global State Object for the Distributed Cinematic Intelligence.
    Tracks everything from character identities to the production status of every shot.
    """
    title: str
    logline: str
    genre: str
    
    # Repositories
    identities: Dict[str, IdentityProfile] = field(default_factory=dict)
    scene_graph: List[SceneNode] = field(default_factory=list)
    shot_history: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_arcs: List[str] = field(default_factory=list)
    
    # Metadata
    history: List[Event] = field(default_factory=list)
    
    def log_event(self, agent: str, action: str, details: str = ""):
        from datetime import datetime
        details_str = str(details)
        event = Event(
            timestamp=datetime.now().isoformat(),
            agent=agent,
            action=action,
            details=details_str
        )
        self.history.append(event)
        logger.info(f"[{agent}] {action}: {details_str[:50]}...")

    def get_identity(self, name: str) -> Optional[IdentityProfile]:
        return self.identities.get(name)

    def register_identity(self, profile: IdentityProfile):
        self.identities[profile.name] = profile
        self.log_event("IdentityManager", "registered_identity", profile.name)

    def save(self, path: Path):
        # Simple serialization
        data = {
            "title": self.title,
            "identities": {k: v.__dict__ for k, v in self.identities.items()},
            # ... complete serialization would go here
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
