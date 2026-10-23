The code below reads log lines from an LLM service and summarizes them, but it crashes. Two real tracebacks are shown here. Read each one **from the bottom**, find the cause, and fix the code inside the two functions.

The first crash comes from `parse_line("model=small tokens=120 latency=0.84s")`:

```text
Traceback (most recent call last):
  File "exercise.py", line 21, in summarize
    records = [parse_line(line) for line in lines]
  File "exercise.py", line 8, in parse_line
    "latency": float(parts["latency"]),
ValueError: could not convert string to float: '0.84s'
```

The second one comes from a list that contains an empty line:

```text
Traceback (most recent call last):
  File "exercise.py", line 21, in summarize
    records = [parse_line(line) for line in lines]
  File "exercise.py", line 7, in parse_line
    "model": parts["model"],
KeyError: 'model'
```

**Example**

| call | result |
|---|---|
| `parse_line("model=a tokens=5 latency=0.5s")` | `{"model": "a", "tokens": 5, "latency": 0.5}` |
| `summarize(["model=a tokens=100 latency=1.0s", "", "model=a tokens=50 latency=2.0s"])` | `(150, 1.5)` |
| `summarize([])` | `(0, 0.0)` |

**Rules**
- Latency may be written with or without a trailing `s`.
- Blank lines and lines with only spaces are skipped.
- Change the code inside the functions; keep their names and what they return.
