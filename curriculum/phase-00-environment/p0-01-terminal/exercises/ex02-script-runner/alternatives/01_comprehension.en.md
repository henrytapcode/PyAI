# List comprehension & unpacking

This alternative expresses `find_python_files` with a single sorted generator expression and builds the command list with list unpacking (`[*runner, clean, *(args or [])]`). It is more compact than appending in a loop while preserving the exact `"/"` folder-boundary check.
