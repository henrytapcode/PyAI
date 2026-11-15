# Stateful `Agent` class with a `step()` method

Instead of holding `messages`, `trace`, `steps`, and `total_tokens` in local variables inside one function, this version wraps the agent state in a class `Agent` with a single-iteration `step()` method. Separating `step()` from `run()` makes it easy to pause between steps, stream progress to a UI, or pause for human approval, at the cost of slightly more boilerplate than a plain function.
