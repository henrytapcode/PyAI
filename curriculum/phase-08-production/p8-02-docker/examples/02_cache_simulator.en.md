# Simulate Docker build cache reuse

**What it shows:** Comparing a well-ordered `Dockerfile` (`COPY requirements.txt .` before `COPY . .`) against a poorly ordered one when only `main.py` is edited.

**Step by step**
1. Lines 3–18 define `GOOD_ORDER` and `BAD_ORDER`, pairing each instruction with the set of project files whose changes affect that step.
2. Lines 21–35 implement `simulate_build(steps, changed_files, has_cache)`: once any step misses the cache (because `has_cache` is `False` or `watched & changed_files` is non-empty), `cache_broken` stays `True` so every later step must `REBUILD`.
3. Lines 38–46 simulate a cold first build and an incremental second build after editing `main.py`, printing `[CACHED]` or `[REBUILD]` per line.

**Notice:** In `BAD ORDER`, editing `main.py` invalidates `COPY . .` at step 3, which also forces `RUN pip install` at step 4 to rebuild even though `requirements.txt` never changed.

**Try it yourself:** Change `{"main.py"}` on line 40 to `{"requirements.txt"}` and verify that both orders now rebuild `RUN pip install` because dependencies actually changed.
