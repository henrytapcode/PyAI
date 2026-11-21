# Explicit key checks

Instead of looping over a `REQUIRED_KEYS` tuple, this version checks each required key with its own `if ... not in parsed:` statement in the exact required order. For a small, fixed set of 3 keys, explicit checks are easy to read; a tuple loop scales better if the list of required keys grows later.
