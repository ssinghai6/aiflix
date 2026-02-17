import logging
import sys
from typing import Any, Dict

def setup_logging(name: str = "AiFlix", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

logger = setup_logging()

def safe_json_parse(response: str) -> Dict[str, Any]:
    """Helper to safely parse JSON from LLM responses (handling potential markdown code blocks)."""
    import json
    import re
    
    # Strip markdown code blocks if present
    cleaned = re.sub(r"```json\s*", "", response)
    cleaned = re.sub(r"```", "", cleaned)
    
    # regex to find the outer-most JSON object
    # This is a simple heuristic: find first { and last }
    start = cleaned.find('{')
    end = cleaned.rfind('}')
    
    if start != -1 and end != -1:
        cleaned = cleaned[start:end+1]
    
    cleaned = cleaned.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        # logger.debug(f"Offending content: {cleaned}")
        return {}
