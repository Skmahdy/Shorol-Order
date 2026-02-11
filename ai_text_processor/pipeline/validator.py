import re
from typing import Dict, List, Any


class ValidationResult:
    """Result of validation."""
    
    def __init__(self, is_valid: bool, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []


class Validator:
    """
    Validate extracted JSON data.
    
    Checks:
    - JSON structure valid
    - orders array exists
    - phone length == 11
    - phone starts with 01
    - quantity is integer (if present)
    - address not empty (if present)
    """
    
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> ValidationResult:
        """
        Validate extracted data.
        
        Args:
            data: Extracted data dictionary
            
        Returns:
            ValidationResult with is_valid flag and errors list
        """
        errors = []
        
        # Check if data is a dictionary
        if not isinstance(data, dict):
            errors.append("Output is not a valid dictionary")
            return ValidationResult(False, errors)
        
        # Check if 'orders' key exists
        if 'orders' not in data:
            errors.append("Missing 'orders' key")
            return ValidationResult(False, errors)
        
        # Check if orders is a list
        if not isinstance(data['orders'], list):
            errors.append("'orders' must be an array")
            return ValidationResult(False, errors)
        
        # Check if orders list is not empty
        if len(data['orders']) == 0:
            errors.append("'orders' array is empty")
            return ValidationResult(False, errors)
        
        # Validate each order
        for idx, order in enumerate(data['orders']):
            order_errors = cls._validate_order(order, idx)
            errors.extend(order_errors)
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, errors)
    
    @classmethod
    def _validate_order(cls, order: Dict[str, Any], idx: int) -> List[str]:
        """Validate a single order."""
        errors = []
        prefix = f"Order {idx}: "
        
        # Check if order is a dictionary
        if not isinstance(order, dict):
            errors.append(f"{prefix}Order is not a valid dictionary")
            return errors
        
        # Validate phone
        if 'phone' in order and order['phone'] is not None:
            phone = str(order['phone']).strip()
            
            # Check phone format (includes length check via regex)
            if not re.match(r'^01[3-9]\d{8}$', phone):
                errors.append(f"{prefix}Phone must be 11 digits starting with 01[3-9]")
        
        # Validate quantity
        if 'quantity' in order and order['quantity'] is not None:
            if not isinstance(order['quantity'], int):
                errors.append(f"{prefix}Quantity must be an integer")
            elif order['quantity'] <= 0:
                errors.append(f"{prefix}Quantity must be positive")
        
        # Validate address (should not be empty if present)
        if 'address' in order and order['address'] is not None:
            address = str(order['address']).strip()
            if len(address) == 0:
                errors.append(f"{prefix}Address cannot be empty")
        
        return errors


# Singleton instance
validator = Validator()
