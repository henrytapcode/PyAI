# Parse log lines with split(): keep errors, pull out fields, summarise.
log = [
    "INFO,gpt-mini,350",
    "ERROR,gpt-large,timeout",
    "INFO,embed,12",
    "ERROR,gpt-mini,rate limit",
]

errors = []
for line in log:
    if line.startswith("ERROR"):
        parts = line.split(",")
        level = parts[0]
        model = parts[1]
        reason = parts[2]
        errors.append(f"{model}: {reason}")

print(f"{len(errors)} errors")
print(" | ".join(errors))
