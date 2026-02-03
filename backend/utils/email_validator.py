import re
from typing import Tuple

class EmailValidator:
    """
    Utility class for additional email validation.
    Complements Pydantic validation (EmailStr).
    """
    
    # Regex pattern for stricter email validation
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # List of disposable email domains (optional)
    DISPOSABLE_DOMAINS = {
        'tempmail.com',
        'guerrillamail.com',
        '10minutemail.com',
        'throwaway.email',
        'mailinator.com',
    }
    
    @staticmethod
    def is_valid_format(email: str) -> Tuple[bool, str]:
        """
        Validates email format using regex.
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not email or len(email) > 254:
            return False, "Invalid email: empty or too long"
        
        if not re.match(EmailValidator.EMAIL_PATTERN, email):
            return False, "Invalid email: incorrect format"
        
        return True, ""
    
    @staticmethod
    def is_disposable(email: str) -> Tuple[bool, str]:
        """
        Checks if email uses a disposable domain.
        
        Returns:
            Tuple[bool, str]: (is_disposable, message)
        """
        domain = email.split('@')[1].lower()
        
        if domain in EmailValidator.DISPOSABLE_DOMAINS:
            return True, f"Email from disposable domain not allowed: {domain}"
        
        return False, ""
    
    @staticmethod
    def validate_email(email: str, check_disposable: bool = False) -> Tuple[bool, str]:
        """
        Performs complete email validation.
        
        Args:
            email: Email to validate
            check_disposable: If True, also validates against disposable domains
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message if any)
        """
        # Validate format
        is_valid, error_msg = EmailValidator.is_valid_format(email)
        if not is_valid:
            return False, error_msg
        
        # Validate against disposable domains (optional)
        if check_disposable:
            is_disposable, error_msg = EmailValidator.is_disposable(email)
            if is_disposable:
                return False, error_msg
        
        return True, ""
