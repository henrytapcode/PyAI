# CLI arguments and exit codes

**What it shows:** how a script receives `argv`-style tokens and returns integer exit codes (`0` for success, non-zero for errors).

**Step by step**
1. `run_cli` checks whether any tokens were provided; if empty, it prints an error and returns `1`.
2. `tokens[0]` is the script name and `tokens[1:]` are the remaining arguments.
3. If the script does not end with `.py`, it returns exit code `2`.
4. Valid inputs print the parsed script and arguments and return `0`.

**Try it yourself:** add `["eval.py", "--fast"]` to the list of samples and check its exit code.
