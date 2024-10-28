import re
from email_validator import validate_email as validate_email_format, EmailNotValidError

def validate_email(email):
    try:
        validate_email_format(email)
        return True
    except EmailNotValidError:
        return False

def validate_password(password):
    if len(password) < 8:
        return False
    # Require at least one number and one letter
    if not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
        return False
    return True