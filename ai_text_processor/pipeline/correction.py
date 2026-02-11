import json
from typing import Dict, Any, List
import os
from openai import OpenAI

from config import config
from pipeline.validator import ValidationResult


class Corrector:
    """
    Correction loop for failed validations.
    
    Prompts AI to fix specific validation errors.
    Max retries = 2
    """
    
    def __init__(self):
        """Initialize corrector with correction prompt."""
        self.correction_prompt_template = self._load_correction_prompt()
        self.client = None
        
        if config.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=config.OPENAI_API_KEY)
            except Exception:
                self.client = None
    
    def _load_correction_prompt(self) -> str:
        """Load correction prompt template from file."""
        try:
            with open(config.CORRECTION_PROMPT_PATH, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback inline prompt
            return """The previous output failed validation.

Errors:
{errors}

Fix ONLY the invalid fields based on the original text below.
Return full valid JSON with "orders" array.
No explanations. No markdown.

Original text:
\"\"\"
{block}
\"\"\"
"""
    
    def retry(self, block: str, validation_result: ValidationResult, retry_count: int = 0) -> Dict[str, Any]:
        """
        Retry extraction with error feedback.
        
        Args:
            block: Original text block
            validation_result: Validation result with errors
            retry_count: Current retry count
            
        Returns:
            Corrected data or status with needs_review
        """
        if retry_count >= config.MAX_RETRIES:
            return {
                "status": "needs_review",
                "errors": validation_result.errors,
                "orders": []
            }
        
        # Format errors as bullet list
        error_list = "\n".join([f"- {error}" for error in validation_result.errors])
        
        # Create correction prompt
        prompt = self.correction_prompt_template.format(
            errors=error_list,
            block=block
        )
        
        try:
            if not self.client:
                # Return mock for testing
                return {
                    "status": "needs_review",
                    "errors": validation_result.errors,
                    "orders": []
                }
            
            response = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=config.TEMPERATURE,
                top_p=config.TOP_P,
                max_tokens=config.MAX_TOKENS
            )
            
            content = response.choices[0].message.content.strip()
            
            # Remove markdown if present
            content = content.replace('```json', '').replace('```', '').strip()
            
            # Parse JSON
            result = json.loads(content)
            
            return result
            
        except Exception as e:
            return {
                "status": "needs_review",
                "errors": validation_result.errors + [f"Correction failed: {str(e)}"],
                "orders": []
            }


# Singleton instance
corrector = Corrector()
