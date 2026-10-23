import pytest

from exercise import parse_line, summarize


def test_parse_line_reads_model_and_tokens():
    record = parse_line("model=small tokens=120 latency=0.5")
    assert record["model"] == "small"
    assert record["tokens"] == 120


def test_parse_line_accepts_latency_without_a_suffix():
    assert parse_line("model=small tokens=120 latency=0.5")["latency"] == pytest.approx(0.5)


def test_parse_line_accepts_latency_with_an_s_suffix():
    record = parse_line("model=small tokens=120 latency=0.84s")
    assert record["latency"] == pytest.approx(0.84), "remove the trailing 's' before float()"


def test_summarize_adds_tokens_and_averages_latency():
    lines = ["model=a tokens=100 latency=1.0s", "model=b tokens=50 latency=2.0s"]
    total, average = summarize(lines)
    assert total == 150
    assert average == pytest.approx(1.5)


def test_summarize_skips_blank_lines():
    lines = ["model=a tokens=10 latency=1.0s", "", "   ", "model=a tokens=30 latency=3.0s"]
    total, average = summarize(lines)
    assert total == 40
    assert average == pytest.approx(2.0), "blank lines are not records, so they do not count"


@pytest.mark.parametrize("lines", [[], [""], ["  ", ""]])
def test_summarize_of_no_records_is_zero(lines):
    assert summarize(lines) == (0, 0.0)
