# Screen and file

**What it shows:** one logger with two handlers. The screen shows only `INFO` and above, while the file keeps every detail from `DEBUG` up.

**Step by step**
1. Lines 6–8 create the logger `pipeline`, let it pass everything from `DEBUG` up, and stop it from sending records to the root logger.
2. Lines 10–12 build the screen handler: it prints to `sys.stdout`, shows `INFO` and above, and uses a short format.
3. Lines 15–25 are a small function that logs a `DEBUG` line per text, a `WARNING` for a long text, and an `INFO` summary.
4. Lines 28–36 create the file handler inside a temporary folder (with a longer format that includes the function name) and add both handlers.
5. Lines 37–42 run the function, and in `finally` remove and close both handlers, so the file is closed even after an error.
6. Lines 44–47 read the file back and print it.

**Notice:** the screen shows two lines, but the file shows five. The logger checks its own level once, then each handler applies its own level.

**Try it yourself:** change `console.setLevel(logging.INFO)` on line 11 to `logging.DEBUG`. The screen should now show the same five messages as the file, with the shorter format.
