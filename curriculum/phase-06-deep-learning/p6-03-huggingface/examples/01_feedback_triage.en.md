# Triaging chatbot user feedback

**What it shows:** Loading a pinned sentiment model offline and classifying six chatbot user replies to count how many negative tickets need attention.

**Step by step**
1. Lines 4–10 load `tokenizer` and `model` from the local cache (`revision=REV, local_files_only=True`) and pass both objects into `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)`.
2. Lines 12–19 list six short user feedback strings in English.
3. Lines 21–28 run `classifier(feedback)` in one call, round each score to 3 decimal places, count the `"NEGATIVE"` replies, and print one line per reply.
4. Line 30 prints the total negative count (`negative count: 3/6`).

**Notice:** Passing the loaded `model` and `tokenizer` objects directly into `pipeline()` guarantees zero network calls while giving you the simple dictionary output (`'label'` and `'score'`).

**Try it yourself:** Add a neutral sentence such as `"The chat window opened at 9 AM."` to `feedback` and see how the binary classifier still forces it into `POSITIVE` or `NEGATIVE`.
