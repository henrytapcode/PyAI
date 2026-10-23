# Default values let the caller skip a parameter; keyword arguments pass by name.
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


def price_with_tax(price, rate=0.1):
    return price + price * rate


print(greet("Lan"))
print(greet("Lan", "Hi"))
print(greet("Lan", greeting="Xin chao"))
print(price_with_tax(100))
print(price_with_tax(100, rate=0.2))
