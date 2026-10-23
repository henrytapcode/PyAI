# Typed chat helpers

**What it shows:** four small functions whose hints describe a conversation: a list of dicts in, a number, a `str | None` or a tuple out.

**Step by step**
1. Lines 2–3 build one message. The return hint `dict[str, str]` says both keys and values are text.
2. Lines 6–10 take a `list[dict[str, str]]` and return an `int`: the total number of words, using an accumulator.
3. Lines 13–18 return `str | None`. If no message has that role, `found` stays `None`, so the hint must allow `None`.
4. Lines 21–22 return a `tuple[int, int]`: two numbers at fixed positions.
5. Lines 25–29 build the conversation. Lines 31–32 show both outcomes of `last_from`.
6. Line 33 unpacks the tuple into `count` and `words`.

**Notice:** the hints tell you what each function returns before you read its body. Line 32 prints `None` because nobody has the role `"system"`.

**Try it yourself:** add `make_message("system", "Be brief.")` to `chat`. Line 32 should now print `Be brief.` instead of `None`.
