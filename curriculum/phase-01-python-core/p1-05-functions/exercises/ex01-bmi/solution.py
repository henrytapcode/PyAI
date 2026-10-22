def bmi(weight_kg, height_m):
    """Return weight divided by height squared."""
    return weight_kg / height_m ** 2


def bmi_category(bmi_value):
    """Return 'underweight', 'normal', 'overweight' or 'obese'."""
    if bmi_value < 18.5:
        return "underweight"
    if bmi_value < 25:
        return "normal"
    if bmi_value < 30:
        return "overweight"
    return "obese"
