# Order assistant with two tools

**What it shows:** Two complete single-round tool loops routing user questions to `lookup_order` or `estimate_delivery` and feeding JSON or text results back to `FakeLLM`.

**Step by step**
1. Lines 6–21 define two local dictionary datasets (`ORDERS` and `CARRIER_DAYS`) and two pure Python lookup functions.
2. Lines 24–39 declare the tool schemas (`TOOLS`) with concise, stopword-free descriptions and register both functions in `REGISTRY`.
3. Lines 42–62 implement `ask_assistant()`: it creates a fresh `FakeLLM()`, runs `chat()` with `tools=TOOLS`, executes the chosen function via `REGISTRY[tc.name](**tc.arguments)`, serializes `dict` results with `json.dumps()`, appends both the `assistant` and `tool` messages, and runs round 2.
4. Lines 65–69 ask one order question and one delivery question, printing the chosen tool, arguments, tool output, and final reply.

**Notice:** Creating a fresh `FakeLLM()` inside `ask_assistant()` keeps every example deterministic and ensures `lookup_order` returning a `dict` is converted to a JSON string before becoming a `tool` message.

**Try it yourself:** Add a third question like `"Tell me a joke"` to the loop on lines 65–68 and watch `ask_assistant()` take the `if not resp.tool_calls:` shortcut.
