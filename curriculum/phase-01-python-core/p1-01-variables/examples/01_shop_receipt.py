# A tiny receipt: variables, arithmetic and f-strings step by step.
item = "coffee"
unit_price = 2.5      # float
quantity = 3          # int

subtotal = unit_price * quantity
tax = subtotal * 0.1
total = subtotal + tax

print(f"{quantity} x {item} @ {unit_price}")
print(f"Subtotal: {subtotal}")
print(f"Tax:      {round(tax, 2)}")
print(f"Total:    {round(total, 2)}")
print(type(total))
