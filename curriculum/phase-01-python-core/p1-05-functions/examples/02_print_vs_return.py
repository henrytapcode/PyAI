# print shows a value on screen; return hands it back to the caller.
def double_print(n):
    print(n * 2)


def double_return(n):
    return n * 2


a = double_print(4)    # prints 8, but a is None
b = double_return(4)   # prints nothing, b is 8
print("a is", a)
print("b is", b)
print("b + 1 =", b + 1)


def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"


print(greet("Lan"))
print(greet("Lan", greeting="Xin chao"))
