# Dates and paths from the standard library, plus the __main__ guard.
from datetime import date, timedelta
from pathlib import Path


def days_left(today, deadline):
    return (deadline - today).days


def describe_file(path_text):
    path = Path(path_text)
    return f"{path.stem} is a {path.suffix} file, folders: {path.parts[:-1]}"


def main():
    start = date(2025, 3, 1)
    deadline = start + timedelta(days=45)
    print("deadline:", deadline)
    print("days left:", days_left(date(2025, 4, 1), deadline))
    print("weekday:", deadline.strftime("%A"))
    print(describe_file("data/raw/reviews.csv"))
    joined = Path("data") / "raw" / "reviews.csv"
    print(joined.name, len(joined.parts))


if __name__ == "__main__":
    main()
