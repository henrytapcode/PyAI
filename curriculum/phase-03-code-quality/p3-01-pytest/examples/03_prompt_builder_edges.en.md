# Edge cases of a prompt builder

**What it shows:** a prompt builder that adds documents until a word budget is used up, tested at its edges with the Arrange, Act, Assert habit and a small `check` helper.

**Step by step**
1. Lines 2–3 define a simple token counter: one token per word.
2. Lines 6–17 define `build_prompt`. It keeps the question, then adds each document while the total stays within `max_tokens`, and stops at the first one that does not fit.
3. Lines 22–29 define `check`, which compares actual and expected and prints PASS or FAIL.
4. Lines 32–34 arrange the data: a 3-word question and two 2-word documents.
5. Lines 36–41 run six checks: no documents, everything fits, an exact fit (5 of 5 words), one word over (4 words), a limit smaller than the question, and an empty question.
6. Line 43 prints the summary.

**Notice:** the most useful checks are the exact fit and one word over. They sit on both sides of the boundary, where an off-by-one mistake would hide.

**Try it yourself:** change `>` to `>=` in line 12 and run again. The exact-fit check turns red, and it is the only one.
