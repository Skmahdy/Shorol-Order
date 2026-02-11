import re
from typing import Dict


class TextCleaner:
    """
    Clean and normalize messy Bangladeshi chat text.
    
    Tasks:
    - Convert Bengali digits to English
    - Remove emojis
    - Normalize spaces
    - Strip +88 prefix
    - Remove repeated punctuation
    """
    
    # Bengali to English digit mapping
    BENGALI_TO_ENGLISH = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
    
    # Emoji pattern (basic Unicode emoji ranges)
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    
    @classmethod
    def clean(cls, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw messy input text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Convert Bengali digits to English
        text = text.translate(cls.BENGALI_TO_ENGLISH)
        
        # Remove emojis
        text = cls.EMOJI_PATTERN.sub('', text)
        
        # Remove +88 prefix from phone numbers (preserve the rest)
        text = re.sub(r'\+88(01[3-9]\d{8})', r'\1', text)
        
        # Remove repeated punctuation (keep max 1)
        text = re.sub(r'([!?.,;:]){2,}', r'\1', text)
        
        # Normalize spaces (multiple spaces to single)
        text = re.sub(r' +', ' ', text)
        
        # Normalize line breaks (multiple line breaks to double)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
