# Logging an LLM call

**What it shows:** a function that calls a (fake) model, retries when it times out, and logs every attempt as `key=value` fields: model, attempt, latency, and size of the reply.

**Step by step**
1. Lines 5–11 set up logging once and create the logger `app.llm`. The format shows the level, the logger name and the message.
2. Lines 13–14 make fake inputs: the first reply is a timeout, and a fake clock gives the same times on every run.
3. Lines 17–21 are the fake model. It raises `TimeoutError` when its reply is `"TIMEOUT"`.
4. Lines 25–31 loop over the attempts. A timeout is logged as a `WARNING` (`llm_retry`) and the loop tries again with `continue`.
5. Lines 32–37 compute the latency from the fake clock, log one `INFO` line (`llm_call`) and return the reply.
6. Line 38 runs only if every attempt failed: that is an `ERROR`, because the operation failed.

**Notice:** the output has a different level for each kind of event, and each message starts with a fixed word (`llm_retry`, `llm_call`, `llm_failed`). That makes the lines easy to search and count later.

**Try it yourself:** change the first reply on line 13 to a normal text. The `WARNING` line should disappear and the `INFO` line should say `attempt=1`.
