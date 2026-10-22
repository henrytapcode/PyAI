def ticket_price(age, is_student):
    """Return the ticket price for a visitor."""
    if age < 5:
        return 0
    elif age < 12 or age >= 65:
        return 6
    elif is_student and age <= 25:
        return 9
    else:
        return 12
