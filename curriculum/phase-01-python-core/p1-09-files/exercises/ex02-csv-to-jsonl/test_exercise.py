import json

import exercise


def make_csv(tmp_path, text):
    path = tmp_path / "scores.csv"
    path.write_text(text, encoding="utf-8")
    return path


def read_records(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def test_returns_the_row_count(tmp_path):
    src = make_csv(tmp_path, "name,score\nLan,9.5\nMinh,7\n")
    assert exercise.csv_to_jsonl(src, tmp_path / "out.jsonl") == 2


def test_writes_one_json_object_per_line(tmp_path):
    src = make_csv(tmp_path, "name,score\nLan,9.5\nMinh,7\n")
    out = tmp_path / "out.jsonl"
    exercise.csv_to_jsonl(src, out)
    lines = out.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2, "each row must become exactly one line"
    assert json.loads(lines[0]) == {"name": "Lan", "score": 9.5}


def test_score_is_a_number_not_text(tmp_path):
    src = make_csv(tmp_path, "name,score\nMinh,7\n")
    out = tmp_path / "out.jsonl"
    exercise.csv_to_jsonl(src, out)
    record = read_records(out)[0]
    assert record["score"] == 7.0
    assert not isinstance(record["score"], str), "convert the score with float()"


def test_empty_csv_gives_empty_file(tmp_path):
    src = make_csv(tmp_path, "name,score\n")
    out = tmp_path / "out.jsonl"
    assert exercise.csv_to_jsonl(src, out) == 0
    assert out.read_text(encoding="utf-8") == ""


def test_keeps_vietnamese_letters(tmp_path):
    src = make_csv(tmp_path, "name,score\nNguyễn Hoa,8\n")
    out = tmp_path / "out.jsonl"
    exercise.csv_to_jsonl(src, out)
    assert "Nguyễn Hoa" in out.read_text(encoding="utf-8"), "use ensure_ascii=False"


def test_overwrites_an_old_output_file(tmp_path):
    src = make_csv(tmp_path, "name,score\nAn,10\n")
    out = tmp_path / "out.jsonl"
    out.write_text("old line\n", encoding="utf-8")
    exercise.csv_to_jsonl(src, out)
    assert read_records(out) == [{"name": "An", "score": 10.0}], 'open the output with "w", not "a"'
