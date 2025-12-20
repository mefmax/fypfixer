import re
from .errors import ValidationError

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def validate_email(email):
    if not email:
        raise ValidationError('Email is required')
    if not EMAIL_REGEX.match(email):
        raise ValidationError('Invalid email format')
    return email.lower().strip()

def validate_password(password):
    if not password:
        raise ValidationError('Password is required')
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters')
    if len(password) > 128:
        raise ValidationError('Password must not exceed 128 characters')
    if not any(c.isalpha() for c in password):
        raise ValidationError('Password must contain at least one letter')
    if not any(c.isdigit() for c in password):
        raise ValidationError('Password must contain at least one number')
    return password

def validate_language(lang):
    if lang not in ['en', 'ru', 'es']:
        raise ValidationError('Language must be en, ru, or es')
    return lang
