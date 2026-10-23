# Embedding batches

**What it shows:** a typical AI preparation step. Clean the documents lazily, then send them to an embedding model in small batches. Here a batch is limited by its total number of characters, not by a fixed number of items.

**Step by step**
1. Lines 2–13 define `batches_by_budget`. It keeps a small list called `batch` and a counter `used` with the characters collected so far.
2. Lines 6–9 run before a text is added: if it would push `used` over `max_chars`, the current batch is yielded and a new empty batch starts.
3. Lines 10–11 add the text to the batch and update `used`. Lines 12–13 yield the leftover batch at the end.
4. Lines 16–17 are a fake embedding call. A real one would return vectors, here it just returns text lengths.
5. Lines 32–33 are two generator expressions: strip every document, then drop the empty ones.
6. Lines 36–39 loop over the batches and print one line per call, with the size of each text and their total.

**Notice:** the batches have different sizes (2, 2 and 3 texts) because short texts fit together and long ones do not. The `batch and` on line 6 keeps us from yielding an empty batch when the very first text is already long.

**Try it yourself:** change the `30` on line 36 to `20`. Every call now holds fewer texts, and you should see six calls.
