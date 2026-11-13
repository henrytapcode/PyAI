# Parse messy price strings into numeric values and report unreadable rows.
import pandas as pd

orders = pd.DataFrame({
    "item": ["notebook", "monitor", "cable", "stand", "keyboard"],
    "price": ["1,200", "N/A", " 350 ", "free", "890"],
})

raw_text = orders["price"].str.replace(",", "", regex=False)
orders["price"] = pd.to_numeric(raw_text, errors="coerce")

bad_count = int(orders["price"].isna().sum())
print("Unreadable prices:", bad_count)

valid = orders.dropna(subset=["price"]).reset_index(drop=True)
valid["price"] = valid["price"].astype("int64")
print(valid)
print("Total valid revenue:", int(valid["price"].sum()))
