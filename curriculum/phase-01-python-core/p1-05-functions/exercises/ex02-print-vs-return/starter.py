# This file has 4 bugs. Run it, call each function, and compare what it SHOWS
# with what it RETURNS.


def area(width, height):
    """Return the area. Example: area(3, 4) returns 12"""
    print(width * height)  # BUG hunt: does this give the number back?


def price_with_tax(price, rate=10):
    """Return the price plus tax. Example: price_with_tax(100) returns 110.0"""
    price * (1 + rate)  # BUG hunt: is the default rate sensible? is anything returned?


def greet(name, greeting="Hello"):
    """Print a greeting. Example: greet("Lan", greeting="Hi") prints Hi, Lan!"""
    print(f"Hello, {name}!")  # BUG hunt: is the greeting parameter used?
