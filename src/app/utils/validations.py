"""
Global Validators.
"""

import re
from email_validator import validate_email, EmailNotValidError

from marshmallow.exceptions import ValidationError


def validate_password_strength(password: str):
    """
    Validate password strength

    Criteria:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At lease one special character
    """

    common_passwords = ["admin@123", "pass@123", "password@123"]

    if len(password) > 64:
        raise ValidationError("Password too long")

    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter")

    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one number")

    if not re.search(r"""[!@#$%^&*(),.?'":{}|<>]""", password):
        raise ValidationError("Password must contain at least one special character")

    if password.lower() in common_passwords:
        raise ValidationError("Password too common.")

    return True, None


def validate_email_format(email: str, allow_disposable=True):
    """
    Validate email format using email-validator library.

    Returns:
        - Normalized email if valid
        - Raises ValueError if invalid
    """

    try:
        valid = validate_email(email, check_deliverability=not allow_disposable)

        return valid.email
    except EmailNotValidError as e:
        raise ValueError(str(e))


def sanitize_input(input_string, max_length=None) -> str:
    """
    Enhanced input sanitization to prevent XSS and SQL injection attacks.

        - Removes dangerous characters
        - Optionally limit input length
        - Handle different input types
    """

    if input_string is None:
        return None

    if not isinstance(input_string, str):
        input_string = str(input_string)

    sanitized = re.sub(r"""[<>&\'"()]""", "", input_string).strip()

    if max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_username(username: str):
    """
    Validate username format

        - Alphanumeric
        - No spaces
        - Reasonable length (3-20 characters)
    """

    if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
        raise ValidationError(
            "Username must be 3-20 characters, alphanumeric or underscore"
        )


def validate_phone_number(phone_number: str):
    """
    Validate phone number format
    Supports various international formats
    """

    phone_regex = r"^\+?\d{1,4}\d{9,15}$"

    if not re.match(phone_regex, phone_number):
        raise ValidationError("Invalid phone number format")
