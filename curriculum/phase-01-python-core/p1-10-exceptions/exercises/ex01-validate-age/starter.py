def validate_age(age):
    """Return age if it is from 0 to 120, otherwise raise a ValueError.

    Example: validate_age(30) returns 30
    """
    if age < 0 or age > 120:
        # TODO 1: replace ___ with the type of error to raise
        raise ___(f"age must be between 0 and 120, got {age}")
    return age


def age_or_none(text):
    """Turn text into a valid age, or return None if that is not possible.

    Example: age_or_none("25") returns 25, age_or_none("x") returns None
    """
    try:
        age = validate_age(int(text))
    # TODO 2: replace ___ with the error type that int("x") and validate_age(200) both raise
    except ___:
        # TODO 3: replace ___ with the value to give back when the text is not a good age
        return ___
    else:
        return age
