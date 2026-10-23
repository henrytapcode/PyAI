# Class roster

**What it shows:** a list of dictionaries (one per student), `.get()` with a default for missing data, and a tuple that is unpacked.

**Step by step**
1. Lines 2–6 build a list with three dicts. The third student, Hoa, has no `"score"` key yet.
2. Lines 8–9 prepare two variables that will remember the best student so far.
3. The loop on lines 10–15 visits each dict. Line 11 reads the score with `.get("score", 0)`, so Hoa gets `0` instead of a `KeyError`.
4. Line 12 prints the name and score. Inside the f-string we use single quotes (`'name'`) because the f-string itself uses double quotes.
5. Lines 13–15 are the "keep the biggest" pattern: if this score beats the best so far, remember it.
6. Line 17 prints the winner. Line 18 packs name and score into a tuple, and line 19 unpacks it again into two variables.

**Notice:** `student["name"]` is safe here because every student has a name. Only `"score"` can be missing, so only that one uses `.get()`.

**Try it yourself:** give Hoa `"score": 10` and run again. The best student should change to Hoa.
