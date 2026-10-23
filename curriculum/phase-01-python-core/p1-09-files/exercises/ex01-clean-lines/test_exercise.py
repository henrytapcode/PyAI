import exercise


def test_strips_spaces_and_newlines(tmp_path):
    path = tmp_path / "prompts.txt"
    path.write_text("  hello \nworld\n", encoding="utf-8")
    assert exercise.read_clean_lines(path) == ["hello", "world"], "use line.strip() on every line"


def test_skips_empty_lines(tmp_path):
    path = tmp_path / "prompts.txt"
    path.write_text("a\n\n   \nb\n", encoding="utf-8")
    assert exercise.read_clean_lines(path) == ["a", "b"], "empty lines must be skipped"


def test_returns_empty_list_for_empty_file(tmp_path):
    path = tmp_path / "empty.txt"
    path.write_text("", encoding="utf-8")
    assert exercise.read_clean_lines(path) == []


def test_last_line_without_newline(tmp_path):
    path = tmp_path / "prompts.txt"
    path.write_text("one\ntwo", encoding="utf-8")
    assert exercise.read_clean_lines(path) == ["one", "two"]


def test_keeps_vietnamese_text(tmp_path):
    path = tmp_path / "vi.txt"
    path.write_text("Xin chào\nTạm biệt\n", encoding="utf-8")
    assert exercise.read_clean_lines(path) == ["Xin chào", "Tạm biệt"], 'use encoding="utf-8"'


def test_works_with_a_string_path(tmp_path):
    path = tmp_path / "prompts.txt"
    path.write_text("x\n", encoding="utf-8")
    assert exercise.read_clean_lines(str(path)) == ["x"]


def test_does_not_change_the_file(tmp_path):
    path = tmp_path / "prompts.txt"
    path.write_text("  a \n\nb\n", encoding="utf-8")
    exercise.read_clean_lines(path)
    assert path.read_text(encoding="utf-8") == "  a \n\nb\n", "only read the file"
