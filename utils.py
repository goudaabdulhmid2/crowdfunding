def validate_required(value, field_name):
    """
    Validate that a required input is not empty.

    This base validation will be reused across the app.
    """
    cleaned_value = value.strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned_value
