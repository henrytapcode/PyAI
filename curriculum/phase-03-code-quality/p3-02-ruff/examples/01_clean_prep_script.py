# A cleaned-up data-prep script: no unused names, None checks with "is", a narrow except.
RAW_LINES = [
    "  Laptop , 999.50 ",
    "Mouse,19.9",
    "Cable,n/a",
    ",5.00",
    "Monitor,249",
]


def parse_price(text: str) -> float | None:
    try:
        return float(text)
    except ValueError:
        return None


def parse_line(line: str) -> tuple[str, float] | None:
    name, price_text = line.split(",")
    name = name.strip()
    price = parse_price(price_text.strip())
    if not name or price is None:
        return None
    return name, price


def load_rows(lines: list[str], skipped: list[str] | None = None) -> list[tuple[str, float]]:
    if skipped is None:
        skipped = []
    rows = []
    for line in lines:
        row = parse_line(line)
        if row is None:
            skipped.append(line.strip())
        else:
            rows.append(row)
    return rows


bad_lines: list[str] = []
good_rows = load_rows(RAW_LINES, bad_lines)
for name, price in good_rows:
    print(f"{name}: {price:.2f}")
print("skipped:", bad_lines)
