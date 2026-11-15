# Separate `_dispatch_call` and `_assistant_tool_message` helpers

Instead of nesting dispatch, error handling, and message formatting inside the `for` loop, this version extracts `_dispatch_call()` and `_assistant_tool_message()` as standalone functions. Separating single-call dispatch from the round loop makes the error-handling logic straightforward to unit-test on its own and easy to reuse across multi-step agents in `p7-07-agents`, at the cost of a couple more function definitions in small scripts.
