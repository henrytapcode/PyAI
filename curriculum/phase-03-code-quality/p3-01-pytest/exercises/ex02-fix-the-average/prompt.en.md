The function `average` below is supposed to return the average of a list of numbers, but the test report is red. Read the failing tests, find the bugs in the code, and fix them. There are two bugs: one shows up with normal input, and one only with an empty list. Change the code inside the function.

The tests are shown in the report under your code. Start from the first red test and read the two sides of its comparison.

**Example**

| call | result |
|---|---|
| `average([1, 2, 3])` | `2.0` |
| `average([5])` | `5.0` |
| `average([])` | raises `ValueError` |

**Rules**
- Return the sum of all numbers divided by how many there are.
- For an empty list, `raise ValueError` instead of dividing by zero.
- Do not change the list you receive.
