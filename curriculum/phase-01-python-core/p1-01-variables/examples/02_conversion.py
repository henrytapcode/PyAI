# Text from a form must be converted before doing maths.
age_text = "21"
height_text = "1.68"

print(age_text + age_text)            # joins text: 2121
age = int(age_text)
height = float(height_text)
print(age + age)                      # real maths: 42
print(f"In 5 years: {age + 5}")
print(f"Height in cm: {height * 100}")
print(type(age), type(height))
