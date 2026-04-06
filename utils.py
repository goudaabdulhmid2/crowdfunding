import re
import database
from datetime import datetime


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
    for user in database.get_users():
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


def validate_positive_number(value, field_name):
    try:
        numeric_value = float(value)
    except ValueError as error:
        raise ValueError(f"{field_name} must be a numeric value.") from error

    if numeric_value <= 0:
        raise ValueError(f"{field_name} must be a positive number.")
    return numeric_value


def validate_date_format(date_str, field_name):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError(f"{field_name} must be a valid date in YYYY-MM-DD format.") from error
    return date_str


def validate_start_end_dates(start_date, end_date):

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start >= end:
        raise ValueError("Start date must be before end date.")
    return start_date, end_date
