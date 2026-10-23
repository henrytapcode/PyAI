def ticket_price(age, is_student):
    """Return the ticket price for a visitor. This code has 3 bugs.

    Rules:
      - under 5 years old: 0
      - under 12, or 65 and older: 6
      - a student aged 25 or less: 9
      - everyone else: 12

    Example: ticket_price(8, False) should return 6
    """
    # TODO: run the tests, then fix the 3 buggy conditions one at a time
    if age <= 5:
        return 0
    elif age < 12 and age >= 65:
        return 6
    elif is_student:
        return 9
    else:
        return 12
