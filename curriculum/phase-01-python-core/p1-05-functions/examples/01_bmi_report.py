# Small functions that call each other: compute BMI, then describe it.
def bmi(weight_kg, height_m):
    """Return the body-mass index."""
    return weight_kg / height_m ** 2


def bmi_category(value):
    """Return a label for a BMI value."""
    if value < 18.5:
        return "underweight"
    if value < 25:
        return "normal"
    return "overweight"


def report(name, weight_kg, height_m):
    value = bmi(weight_kg, height_m)   # one function calls another
    label = bmi_category(value)
    return f"{name}: BMI {value:.1f} ({label})"


print(report("Lan", 52, 1.60))
print(report("Minh", 85, 1.75))
print(report("An", 45, 1.80))
