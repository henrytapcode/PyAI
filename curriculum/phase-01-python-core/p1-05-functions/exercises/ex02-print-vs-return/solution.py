def area(width, height):
    return width * height


def price_with_tax(price, rate=0.1):
    return price * (1 + rate)


def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")
