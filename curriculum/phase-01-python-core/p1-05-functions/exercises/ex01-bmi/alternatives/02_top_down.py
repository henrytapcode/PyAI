def bmi(weight_kg, height_m):
    height_squared = height_m ** 2
    return weight_kg / height_squared


def bmi_category(bmi_value):
    if bmi_value >= 30:
        return "obese"
    if bmi_value >= 25:
        return "overweight"
    if bmi_value >= 18.5:
        return "normal"
    return "underweight"
