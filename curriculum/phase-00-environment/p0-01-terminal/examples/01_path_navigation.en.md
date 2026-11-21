# Navigating paths with PurePosixPath

**What it shows:** how Python represents a terminal's current working directory, parent folder, and joined relative paths without touching the real filesystem.

**Step by step**
1. Line 3 creates a `PurePosixPath` representing the `cwd`.
2. Lines 5–6 inspect `.parent` (what `cd ..` moves to) and `.parts` (each folder segment).
3. Line 8 joins relative segments `"src"` and `"main.py"` with `/`.
4. Lines 10–12 read the file's `.name`, `.suffix`, and check `.is_absolute()`.

**Try it yourself:** change `main_file` to `cwd.parent / "shared" / "utils.py"` and run again to see the new path and parent.
