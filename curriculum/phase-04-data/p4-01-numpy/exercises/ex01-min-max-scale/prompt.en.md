Feature scaling puts numbers on a common `[0, 1]` scale before feeding them to a model. Complete `min_max_scale(values)` by replacing every `___` blank so it shifts and scales `values` using `(values - min) / (max - min)`. Write your code inside the function and `return` the answer.

**Example**

| input | output |
|---|---|
| `np.array([10, 20, 30])` | `array([0.0, 0.5, 1.0])` |

**Rules**
- Keep the same `shape` as `values` (works for both 1D and 2D arrays).
- Do not modify the input array in place.
- Assume `values.max() > values.min()`.
