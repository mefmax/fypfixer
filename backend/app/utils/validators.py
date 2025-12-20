import re
from .errors import ValidationError

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

# SECURITY: Common weak passwords to reject
WEAK_PASSWORDS = {
    'password', 'password1', 'password123', '12345678', '123456789',
    'qwerty123', 'letmein', 'welcome', 'admin123', 'iloveyou',
    'sunshine', 'princess', 'football', 'monkey123', 'dragon123',
}


def validate_email(email):
    if not email:
        raise ValidationError('Email is required')
    if not EMAIL_REGEX.match(email):
        raise ValidationError('Invalid email format')
    return email.lower().strip()


def validate_password(password):
    """
    SECURITY: Strong password validation.
    Requirements:
    - At least 10 characters (was 8)
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    - Not in common weak passwords list
    """
    if not password:
        raise ValidationError('Password is required')

    if len(password) < 10:
        raise ValidationError('Password must be at least 10 characters')

    if len(password) > 128:
        raise ValidationError('Password must not exceed 128 characters')

    # SECURITY: Check for weak passwords
    if password.lower() in WEAK_PASSWORDS:
        raise ValidationError('This password is too common. Please choose a stronger password.')

    if not any(c.isupper() for c in password):
        raise ValidationError('Password must contain at least one uppercase letter')

    if not any(c.islower() for c in password):
        raise ValidationError('Password must contain at least one lowercase letter')

    if not any(c.isdigit() for c in password):
        raise ValidationError('Password must contain at least one number')

    # SECURITY: Require special character
    special_chars = set('!@#$%^&*()_+-=[]{}|;:,.<>?/~`')
    if not any(c in special_chars for c in password):
        raise ValidationError('Password must contain at least one special character (!@#$%^&*...)')

    return password


def validate_language(lang):
    if lang not in ['en', 'ru', 'es']:
        raise ValidationError('Language must be en, ru, or es')
    return lang


def sanitize_string(value: str, max_length: int = 255) -> str:
    """SECURITY: Sanitize user input string."""
    if not value:
        return ''
    # Remove null bytes and control characters
    value = ''.join(c for c in value if c.isprintable() or c in '\n\t')
    # Truncate to max length
    return value[:max_length].strip()
