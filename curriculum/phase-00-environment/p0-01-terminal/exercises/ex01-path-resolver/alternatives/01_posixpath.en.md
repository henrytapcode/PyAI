# Standard library `posixpath.normpath`

Instead of managing a segment stack manually, this alternative delegates `.` and `..` collapsing to Python's built-in `posixpath.normpath`. One subtle POSIX quirk: `normpath("//a")` preserves a leading double slash `//a`, so the `while` loop strips any extra leading `/`. Both solutions produce identical output.
