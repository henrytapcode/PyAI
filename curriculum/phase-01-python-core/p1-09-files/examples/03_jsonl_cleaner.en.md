# JSON config and a JSON Lines cleaner

**What it shows:** `json.dump` / `json.load` for a config file, and a line-by-line cleaning job on a `.jsonl` dataset.

**Step by step**
1. Lines 6–12 prepare a config dict and four training examples, one with an empty response.
2. Lines 19–22 save the config with `json.dump` and load it back with `json.load`. `ensure_ascii=False` keeps the Vietnamese letters.
3. Lines 24–26 write the raw dataset: one `json.dumps(item) + "\n"` per example.
4. Line 29 opens the source and the destination in one `with`.
5. Lines 30–34 read each line with `json.loads(line)` and write it to the clean file only if the response is at least `min_length` characters long.
6. Lines 36–38 print the count and print the prompts that survived.

**Notice:** the threshold comes from the config file, not from the code. To change the rule you edit the data, not the program.

**Try it yourself:** set `"min_length": 1` in `config`. The response `"ok"` is now long enough, so you should see `kept 3 of 4`.
