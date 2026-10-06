def validate_age(age: float) -> float:
    """Validate that age is within a plausible human range."""
    if age <= 0 or age > 120:
        raise ValueError("Age must be between 0 and 120.")

    return age
