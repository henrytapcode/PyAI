# if / elif / else: the first matching branch wins.
temperature = 31
is_raining = False

if temperature >= 35:
    advice = "Too hot, stay inside"
elif temperature >= 25:
    advice = "Warm day"
elif temperature >= 15:
    advice = "Mild day"
else:
    advice = "Take a jacket"

print(f"{temperature} degrees: {advice}")

if is_raining:
    print("Bring an umbrella")
else:
    print("No umbrella needed")
