# Summarize a ruff report: parse each short-form line and count by rule code and by file.
REPORT = [
    "prep.py:1:8: F401 [*] `os` imported but unused",
    "prep.py:5:26: B006 Do not use mutable data structures for argument defaults",
    "prep.py:13:5: E722 Do not use bare `except`",
    "prep.py:15:5: F841 Local variable `total` is assigned to but never used",
    "util.py:3:1: F401 [*] `json` imported but unused",
    "util.py:9:16: E711 Comparison to `None` should be `cond is None`",
]


def parse_line(line: str) -> tuple[str, str, bool]:
    file_name, _line_number, _column, rest = line.split(":")
    words = rest.split()
    return file_name, words[0], "[*]" in words


by_code: dict[str, int] = {}
by_file: dict[str, int] = {}
fixable = 0
for report_line in REPORT:
    file_name, code, is_fixable = parse_line(report_line)
    by_code[code] = by_code.get(code, 0) + 1
    by_file[file_name] = by_file.get(file_name, 0) + 1
    if is_fixable:
        fixable += 1

print("by code:")
for code in sorted(by_code):
    print(" ", code, by_code[code])
print("by file:")
for file_name in sorted(by_file):
    print(" ", file_name, by_file[file_name])
print("fixable with --fix:", fixable, "of", len(REPORT))
