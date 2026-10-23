`make_slug(title)` should turn a title into a URL slug: all lowercase, extra spaces removed, words joined by a single hyphen. The code runs, but it gives wrong answers. Find the bugs and fix them.

**Example**

| call | returns |
|---|---|
| `make_slug("Hello World")` | `"hello-world"` |
| `make_slug("  Python   For AI  ")` | `"python-for-ai"` |

**Rules**
- Fix the code inside the function and `return` the slug (do not `print` it).
- There is more than one bug. Press **Check** to see which tests still fail.
