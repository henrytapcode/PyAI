# FAQ response cache with normalized keys

**What it shows:** Caching 12 incoming support questions with `FakeLLM` using normalized SHA-256 keys so extra spaces still hit the cache, then printing per-request `HIT`/`MISS` lines and overall hit rate.

**Step by step**
1. Lines 9–21 define `normalize_question` (trimming outer whitespace and collapsing repeated spaces) and `make_faq_key` (serializing `model`, normalized `system`, normalized `question`, and `temperature=0.0` with `json.dumps(..., sort_keys=True)` before SHA-256 hashing).
2. Lines 24–45 initialize `FakeLLM`, the cache dictionary, and 12 FAQ questions including exact repeats and whitespace variants like `'  What is   RAG? '`.
3. Lines 47–68 look up each key, increment `hits` or call `client.chat(...)` on a `MISS`, print each decision, and summarize `hit_rate=0.50`.

**Notice:** `'  What is   RAG? '` hits the entry saved for `'What is RAG?'` because `normalize_question` collapses whitespace before hashing, while casing and punctuation stay untouched.

**Try it yourself:** Add a repeated whitespace variant of `"What is tool calling?"` (such as `"  What is   tool calling?  "`) to `questions` and run again to see `hit_rate` rise from `0.50` to `0.54`.
