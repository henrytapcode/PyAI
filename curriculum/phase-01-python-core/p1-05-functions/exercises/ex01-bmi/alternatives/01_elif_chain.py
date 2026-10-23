def bmi(weight_kg, height_m):
    return weight_kg / (height_m * height_m)


def bmi_category(bmi_value):
    if bmi_value < 18.5:
        label = "underweight"
    elif bmi_value < 25:
        label = "normal"
    elif bmi_value < 30:
        label = "overweight"
    else:
        label = "obese"
    return label
