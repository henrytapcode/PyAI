The function `ticket_price(age, is_student)` should follow these rules:

- under 5 years old: free (`0`)
- under 12, **or** 65 and older: `6`
- a student aged 25 or less: `9`
- everyone else: `12`

The code below has **3 bugs**. Run the tests, find them and fix them. Write your fixes **inside the function**; it uses `return` to give back the price (you will learn functions properly in lesson 5).

**Example**

| Call | Returns |
|---|---|
| `ticket_price(3, False)` | `0` |
| `ticket_price(8, False)` | `6` |
| `ticket_price(20, True)` | `9` |
| `ticket_price(30, True)` | `12` |

**Rules**
- Return a number: `0`, `6`, `9` or `12`.
- Keep the same structure (`if` / `elif` / `else`); only fix the conditions.
