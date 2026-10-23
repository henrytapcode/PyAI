# Clean a list of messy form values: convert what we can, count what we cannot.
def safe_int(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default


raw_values = ["12", " 7 ", "twelve", "", None, "40"]

numbers = []
bad_count = 0
for raw in raw_values:
    value = safe_int(raw, default=None)
    if value is None:
        bad_count += 1
    else:
        numbers.append(value)

print("clean:", numbers)
print("bad values:", bad_count)
print("sum:", sum(numbers))
