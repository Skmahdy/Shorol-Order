import json
from typing import Dict, Any, Optional
import os
try:
    import openai
except ImportError:
    openai = None

from config import config


class Extractor:
    """
    AI-based extraction layer using OpenAI.
    
    Loads system prompt from file.
    Uses deterministic settings (low temperature).
    """
    
    def __init__(self):
        """Initialize the extractor with system prompt."""
        self.system_prompt = self._load_system_prompt()
        
        if openai and config.OPENAI_API_KEY:
            openai.api_key = config.OPENAI_API_KEY
    
    def _load_system_prompt(self) -> str:
        """Load system prompt from file."""
        try:
            with open(config.SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback inline prompt
            return """You are an order extraction engine for Bangladesh F-commerce.

Rules:
1. Output ONLY valid JSON.
2. No markdown.
3. No explanations.
4. Do not guess missing values.
5. Convert Bengali digits to English.
6. Phone must contain digits only.
7. Always return array "orders".
8. Do not merge separate customers."""
    
    def extract(self, block: str) -> Dict[str, Any]:
        """
        Extract structured data from text block using AI.
        
        Args:
            block: Text block to extract from
            
        Returns:
            Extracted data as dict
        """
        user_prompt = f"""Extract structured delivery order from this message:

\"\"\"
{block}
\"\"\"
"""
        
        try:
            if not openai or not config.OPENAI_API_KEY:
                # Return mock response for testing without API key
                return self._extract_mock(block)
            
            response = openai.ChatCompletion.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
                max_tokens=config.MAX_TOKENS
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            content = content.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            # Return error structure
            return {
                "error": str(e),
                "orders": []
            }
    
    def _extract_mock(self, block: str) -> Dict[str, Any]:
        """Mock extraction for testing without API key."""
        import re
        
        # Try to extract phone
        phone_match = re.search(r'01[3-9]\d{8}', block)
        phone = phone_match.group(0) if phone_match else None
        
        # Simple extraction
        return {
            "orders": [
                {
                    "customer_name": None,
                    "phone": phone,
                    "address": None,
                    "item": None,
                    "quantity": None,
                    "notes": block[:50] if len(block) > 50 else block
                }
            ]
        }


# Singleton instance
extractor = Extractor()
