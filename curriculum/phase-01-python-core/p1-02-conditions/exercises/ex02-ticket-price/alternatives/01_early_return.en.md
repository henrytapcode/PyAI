# Early returns instead of `elif`

Each rule is its own `if` that returns straight away, and the last line handles "everyone else". The logic is the same as the `elif` chain: once a rule matches, `return` ends the function, so the later rules are never tested. Some people find this flatter and easier to read.
