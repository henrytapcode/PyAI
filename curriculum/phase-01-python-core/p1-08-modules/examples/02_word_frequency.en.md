# Word frequencies with Counter

**What it shows:** a ready-made tool from the standard library doing the job you coded by hand in the collections lesson.

**Step by step**
1. Line 2 imports one name, `Counter`, from the `collections` module.
2. Line 4 is a sentence. Line 5 uses `text.split()` to cut it into a list of words.
3. Line 7 builds the counter in one go: `Counter(words)` is the whole `counts.get(word, 0) + 1` loop. It behaves like a dict from word to count.
4. Line 9 prints the whole counter, most frequent word first. Line 10 reads one count like a dict: `4`. Line 11 asks for a missing word and gets `0`, **not** a `KeyError`.
5. Line 12 `most_common(2)` returns a list of `(word, count)` tuples for the 2 biggest counts.
6. Lines 14–15 loop over those tuples and unpack each into `word` and `number`. In the f-string, `:<4` pads the word to 4 characters so the numbers line up.

**Notice:** when words tie (`sat` and `on` both appear twice), Counter keeps the order in which it first saw them.

**Try it yourself:** replace `text` with a sentence of your own and print `counts.most_common(1)`.
