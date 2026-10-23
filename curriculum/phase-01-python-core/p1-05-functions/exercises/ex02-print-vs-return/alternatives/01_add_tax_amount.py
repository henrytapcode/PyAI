def area(width, height):
    result = width * height
    return result


def price_with_tax(price, rate=0.1):
    tax = price * rate
    return price + tax


def greet(name, greeting="Hello"):
    print(greeting + ", " + name + "!")
