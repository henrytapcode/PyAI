# A usage report with aligned columns, thousands separators and money format.
usage = {
    "gpt-mini": {"tokens": 1250000, "price_per_million": 0.15},
    "gpt-large": {"tokens": 48200, "price_per_million": 5.0},
    "embed": {"tokens": 910, "price_per_million": 0.02},
}

print(f"{'model':<12}{'tokens':>12}{'cost (USD)':>14}")
total = 0
for model in usage:
    tokens = usage[model]["tokens"]
    cost = tokens / 1000000 * usage[model]["price_per_million"]
    total = total + cost
    print(f"{model:<12}{tokens:>12,}{cost:>14.4f}")

print("-" * 38)
print(f"{'total':<24}{total:>14.4f}")
