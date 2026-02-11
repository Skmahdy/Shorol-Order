import re
from typing import List


class BatchSplitter:
    """
    Split text into blocks based on phone numbers or line breaks.
    
    Primary rule: Split by valid BD phone numbers.
    Secondary rule: Split by double line breaks.
    """
    
    # Bangladesh phone number pattern
    # Matches: 01[3-9]xxxxxxxxx (11 digits starting with 01)
    PHONE_PATTERN = re.compile(r'(\+?88)?01[3-9]\d{8}')
    
    @classmethod
    def split(cls, text: str) -> List[str]:
        """
        Split text into blocks.
        
        Args:
            text: Cleaned text
            
        Returns:
            List of text blocks
        """
        if not text:
            return []
        
        # Find all phone numbers and their positions
        phone_matches = list(cls.PHONE_PATTERN.finditer(text))
        
        if len(phone_matches) > 1:
            # Multiple phone numbers found - split around them
            blocks = []
            
            for i, match in enumerate(phone_matches):
                # Get start position of current phone
                start_pos = match.start()
                
                # Get end position (start of next phone or end of text)
                if i < len(phone_matches) - 1:
                    end_pos = phone_matches[i + 1].start()
                else:
                    end_pos = len(text)
                
                # Extract block
                block = text[start_pos:end_pos].strip()
                if block:
                    blocks.append(block)
            
            return blocks
        
        elif len(phone_matches) == 1:
            # Single phone number - return as single block
            return [text.strip()]
        
        else:
            # No phone numbers found - split by double line breaks
            blocks = [block.strip() for block in text.split('\n\n') if block.strip()]
            return blocks if blocks else [text.strip()]
