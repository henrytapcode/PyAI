# A safe request log

**What it shows:** how to log a model request with useful fields (model and tokens through `extra=`) while keeping the secret key and the private prompt out of the log.

**Step by step**
1. Lines 5–10 set up the format. After the message it prints two extra fields, `model` and `tokens`, which come from `extra=`.
2. Lines 14–15 define `mask_key`. It keeps only the last four characters of the key, with `...` in front.
3. Lines 18–24 log a request. The message holds the masked key and the **length** of the prompt, never the prompt itself. The `extra` dict supplies `model` and `tokens`.
4. Lines 27–32 log a failure at `ERROR` level. This record must also carry `model` and `tokens`, because the format needs them.
5. Lines 35–36 call both functions with a fake key and a prompt that contains an email address.

**Notice:** the output contains neither the full key nor the email address. A log is read by many people and tools, so it should only contain what they are allowed to see.

**Try it yourself:** delete `"tokens": 0` from the `extra` dict on line 31 and run again. Logging prints an error about the missing field instead of your message, which is why every record needs the same extra fields.
