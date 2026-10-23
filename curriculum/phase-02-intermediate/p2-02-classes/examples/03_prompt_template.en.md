# Prompt templates

**What it shows:** an object that remembers settings (its template text) and also counts how often it was used.

**Step by step**
1. Lines 3–6 store three attributes. `template` is the text with `{topic}` and `{audience}` placeholders; `uses` starts at 0.
2. Line 9 adds 1 to `self.uses` every time `fill` runs, so the object keeps count of its own calls.
3. Lines 10–11 replace the two placeholders one after the other and return the finished prompt.
4. Lines 17–18 build two different templates from one class.
5. Lines 20–22 fill them in. `explain` is used twice and `quiz` once.
6. Lines 23–24 print the objects. `__repr__` shows `uses`, so you can see the counts.

**Notice:** the placeholder text such as `"{topic}"` is in a normal string, not an f-string, so Python leaves the braces alone and `replace` can find them.

**Try it yourself:** build `summary = PromptTemplate("summary", "Summarise {topic} for {audience}.")`, fill it once and print it. You should see `uses=1`.
