import os
from typing import Optional

class Config:
    """Configuration for AI text processor"""
    
    # API Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    
    # Model Settings (Deterministic)
    TEMPERATURE: float = 0.1
    TOP_P: float = 0.3
    MAX_TOKENS: int = 2000
    
    # Processing Settings
    MAX_RETRIES: int = 2
    
    # Paths
    PROMPTS_DIR: str = os.path.join(os.path.dirname(__file__), "prompts")
    SYSTEM_PROMPT_PATH: str = os.path.join(PROMPTS_DIR, "system_prompt.txt")
    CORRECTION_PROMPT_PATH: str = os.path.join(PROMPTS_DIR, "correction_prompt.txt")

config = Config()
