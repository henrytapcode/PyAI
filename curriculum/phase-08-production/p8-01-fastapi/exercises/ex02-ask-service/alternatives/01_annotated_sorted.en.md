# Reusable Annotated types with set comprehension and sorted()

This alternative (previewing Python's `typing.Annotated`) attaches `Field(...)` rules to reusable type aliases (`QuestionText`, `TopK`) and computes `ranked` with a comprehension plus `sorted(..., key=...)` instead of building a list in a `for` loop. Choose `Annotated` when several Pydantic models share the exact same field constraints, and stick to inline `= Field(...)` plus a plain `for` loop when you only use a schema once or want easier step-by-step debugging.
