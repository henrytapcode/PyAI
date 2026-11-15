# Step-by-step state class

This alternative isolates per-turn agent state inside `_AgentSession` with a single `step()` method returning either a stop reason or `None`, and drives expectation checks from a declarative `(label, failed)` table. Splitting a single turn into `step()` makes it easy to pause, inspect intermediate state, or resume after human approval in larger applications.
