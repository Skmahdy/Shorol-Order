import re
from typing import Dict, Any
import copy


class AutoFixer:
    """
    Deterministic auto-fixer for common BD issues.
    
    Fixes:
    - Phone without leading 0
    - Phone with +88 prefix
    - Quantity extraction from item text
    """
    
    @classmethod
    def auto_fix(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply deterministic fixes to data.
        
        Args:
            data: Data to fix
            
        Returns:
            Fixed data
        """
        # Deep copy to avoid modifying original
        fixed_data = copy.deepcopy(data)
        
        if 'orders' not in fixed_data or not isinstance(fixed_data['orders'], list):
            return fixed_data
        
        for order in fixed_data['orders']:
            if not isinstance(order, dict):
                continue
            
            # Fix phone
            order['phone'] = cls._fix_phone(order.get('phone'))
            
            # Fix quantity from item text
            if order.get('quantity') is None and order.get('item'):
                order['quantity'] = cls._extract_quantity_from_item(order['item'])
        
        return fixed_data
    
    @classmethod
    def _fix_phone(cls, phone: Any) -> Any:
        """
        Fix common phone number issues.
        
        Args:
            phone: Phone number to fix
            
        Returns:
            Fixed phone number
        """
        if phone is None:
            return None
        
        phone_str = str(phone).strip()
        
        # Remove +88 prefix
        phone_str = re.sub(r'^\+?88', '', phone_str)
        
        # Remove spaces and dashes
        phone_str = phone_str.replace(' ', '').replace('-', '')
        
        # If starts with 1 and is 10 digits, prepend 0
        if re.match(r'^1[3-9]\d{8}$', phone_str):
            phone_str = '0' + phone_str
        
        # Remove any non-digit characters
        phone_str = re.sub(r'\D', '', phone_str)
        
        # Only return if it looks like a valid BD phone
        if re.match(r'^01[3-9]\d{8}$', phone_str):
            return phone_str
        
        return phone if phone else None
    
    @classmethod
    def _extract_quantity_from_item(cls, item: str) -> Any:
        """
        Extract quantity from item text.
        
        Args:
            item: Item text
            
        Returns:
            Extracted quantity or None
        """
        if not item:
            return None
        
        item_lower = item.lower()
        
        # Try to extract numbers followed by "pc", "pcs", "piece", etc.
        patterns = [
            r'(\d+)\s*(?:pc|pcs|piece|pieces)',
            r'(\d+)\s*(?:ta|ti|taa)',  # Bangla: "ta", "ti"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, item_lower)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    pass
        
        # Try Bengali words for numbers
        bengali_numbers = {
            'ek': 1, 'ekta': 1, 'ekti': 1,
            'dui': 2, 'duita': 2, 'duiti': 2,
            'tin': 3, 'tinta': 3, 'tinti': 3,
            'char': 4, 'charta': 4, 'charti': 4,
            'panch': 5, 'panchta': 5, 'panchti': 5,
        }
        
        for word, num in bengali_numbers.items():
            if word in item_lower:
                return num
        
        return None


# Singleton instance
fixer = AutoFixer()
