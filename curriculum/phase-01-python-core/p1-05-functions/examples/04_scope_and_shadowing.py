# Local variables, global variables, and a local that hides a global.
rate = 0.1                  # global: visible everywhere


def add_tax(price):
    tax = price * rate      # tax is local; rate is read from the global
    return price + tax


def broken_reset():
    rate = 0                # a NEW local variable that hides the global one
    return rate


print(add_tax(100))
print(broken_reset())
print(rate)
