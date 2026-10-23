# Token stream

**What it shows:** a generator that hands out a reply one token at a time, like a chatbot that types its answer.

**Step by step**
1. Lines 2–4 define `stream_reply`. It cuts the text into words and `yield`s them one by one. Nothing runs yet when you call it.
2. Line 8 creates the generator object. Line 10 asks for the first token with `next`.
3. Lines 13–14 use a `for` loop on the same generator. It continues from the second token, because the first one is already taken.
4. Line 16 calls `stream_reply` again to get a **fresh** generator and glues all its tokens together with `"".join(...)`.

**Notice:** the loop on lines 13–14 does not print `Generators` again. The generator remembers its position, so it only gives what is left.

**Try it yourself:** add a second `for token in stream:` loop after line 14 and run it. It prints nothing, because the generator is already exhausted.
