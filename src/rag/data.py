from dataclasses import dataclass
from typing import List

@dataclass
class KnowledgeItem:
    category: str
    title: str
    author: str
    content: str
    tags: List[str]

# Initial seed data for the in-memory RAG
# In a full system, this would be loaded from PDFs into a vector DB
SEED_KNOWLEDGE = [
    KnowledgeItem(
        category="Screenwriting",
        title="Three-Act Structure",
        author="Syd Field",
        content="The paradigm of the three-act structure breaks the screenplay into Setup (Act I), Confrontation (Act II), and Resolution (Act III). Key plot points connect these acts. Plot Point I disrupts the status quo, and Plot Point II leads to the climax.",
        tags=["structure", "plot", "foundation"]
    ),
    KnowledgeItem(
        category="Screenwriting",
        title="The Hero's Journey",
        author="Joseph Campbell",
        content="The monomyth where a hero ventures forth from the world of common day into a region of supernatural wonder: fabulous forces are there encountered and a decisive victory is won.",
        tags=["myth", "character_arc", "archetype"]
    ),
    KnowledgeItem(
        category="Cinematography",
        title="Rembrandt Lighting",
        author="Standard Technique",
        content="A lighting technique that characterizes a small, inverted triangle of light on the shadowed cheek of the subject. It creates a dramatic, moody feel, often used in film noir or emotional scenes.",
        tags=["lighting", "drama", "technique"]
    ),
    KnowledgeItem(
        category="Cinematography",
        title="Dutch Angle",
        author="Standard Technique",
        content="The camera is set at an angle on its roll axis so that the shot is composed with vertical lines at an angle to the side of the frame, or so that the horizon line of the shot is not parallel with the bottom of the camera frame. Creates tension or disorientation.",
        tags=["camera_angle", "tension", "composition"]
    ),
    KnowledgeItem(
        category="Cinematography",
        title="Teal and Orange",
        author="Color Theory",
        content="A color grading look that uses complementary colors (teal used for shadows/backgrounds, orange for highlights/skin tones) to create high contrast and visual separation.",
        tags=["color", "grading", "aesthetic"]
    )
]
