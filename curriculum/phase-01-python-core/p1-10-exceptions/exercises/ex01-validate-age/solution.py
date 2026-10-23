def validate_age(age):
    """Return age if it is from 0 to 120, otherwise raise a ValueError.

    Example: validate_age(30) returns 30
    """
    if age < 0 or age > 120:
        raise ValueError(f"age must be between 0 and 120, got {age}")
    return age


def age_or_none(text):
    """Turn text into a valid age, or return None if that is not possible.

    Example: age_or_none("25") returns 25, age_or_none("x") returns None
    """
    try:
        age = validate_age(int(text))
    except ValueError:
        return None
    else:
        return age
