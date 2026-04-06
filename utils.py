import re
from database import users


def validate_required(value, field_name):

    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned_value


def validate_email(email):

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format.")
    return email

def validate_email_is_unique(email):
    for user in users:
        if user["email"] == email:
            raise ValueError("Email already exists.")
    return email


def validate_password_confirmation(password, confirm_password):
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    return password

def validate_egyptian_phone(phone):
    phone_pattern = r'^(010|011|012|015)\d{8}$'
    if not re.match(phone_pattern, phone):
        raise ValueError("Invalid Egyptian phone number format.")
    return phone
