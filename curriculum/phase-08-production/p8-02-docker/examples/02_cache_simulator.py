# Compare build cache reuse when only main.py changes.

GOOD_ORDER = [
    ("FROM python:3.13-slim", set()),
    ("WORKDIR /app", set()),
    ("COPY requirements.txt .", {"requirements.txt"}),
    ("RUN pip install --no-cache-dir -r requirements.txt", set()),
    ("COPY . .", {"main.py", "requirements.txt"}),
    ('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]', set()),
]

BAD_ORDER = [
    ("FROM python:3.13-slim", set()),
    ("WORKDIR /app", set()),
    ("COPY . .", {"main.py", "requirements.txt"}),
    ("RUN pip install --no-cache-dir -r requirements.txt", set()),
    ('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]', set()),
]


def simulate_build(
    steps: list[tuple[str, set[str]]],
    changed_files: set[str],
    has_cache: bool,
) -> list[tuple[str, str]]:
    """Return (status, instruction) for each step in a Docker build."""
    cache_broken = not has_cache
    report: list[tuple[str, str]] = []
    for inst, watched in steps:
        if cache_broken or (watched & changed_files):
            cache_broken = True
            report.append(("REBUILD", inst))
        else:
            report.append(("CACHED", inst))
    return report


for label, plan in [("GOOD ORDER", GOOD_ORDER), ("BAD ORDER", BAD_ORDER)]:
    first_build = simulate_build(plan, set(), has_cache=False)
    second_build = simulate_build(plan, {"main.py"}, has_cache=True)
    rebuilt_1 = sum(1 for status, _ in first_build if status == "REBUILD")
    rebuilt_2 = sum(1 for status, _ in second_build if status == "REBUILD")
    print(f"=== {label} (Build 1 cold: {rebuilt_1} rebuilt) ===")
    for idx, (status, inst) in enumerate(second_build, 1):
        print(f"  {idx}. [{status:<7}] {inst}")
    print(f"Build 2 (main.py edited) rebuilt layers: {rebuilt_2}/{len(plan)}\n")
