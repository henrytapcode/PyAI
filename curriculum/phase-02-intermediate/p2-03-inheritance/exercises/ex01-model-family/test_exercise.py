import pytest

from exercise import CannedModel, Model


def test_model_stores_its_name():
    assert Model("base").name == "base"


def test_model_describe_uses_the_name():
    assert Model("base").describe() == "model: base"


def test_model_generate_must_be_written_by_children():
    with pytest.raises(NotImplementedError):
        Model("base").generate("hi")


def test_canned_model_is_a_model():
    assert isinstance(CannedModel("c1", ["Hi!"]), Model)


def test_canned_model_gets_its_name_from_the_parent():
    bot = CannedModel("canned-1", ["Hi!"])
    assert bot.name == "canned-1", "call super().__init__(name) so the parent stores the name"


def test_canned_model_keeps_its_replies():
    assert CannedModel("c1", ["a", "b"]).replies == ["a", "b"]


def test_replies_come_back_in_order():
    bot = CannedModel("c1", ["a", "b", "c"])
    assert bot.generate("x") == "a"
    assert bot.generate("x") == "b"
    assert bot.generate("x") == "c"


def test_replies_start_over_after_the_last_one():
    bot = CannedModel("c1", ["Hi!", "Bye!"])
    got = [bot.generate("x") for _ in range(5)]
    assert got == ["Hi!", "Bye!", "Hi!", "Bye!", "Hi!"]


def test_the_prompt_is_ignored():
    bot = CannedModel("c1", ["a", "b"])
    assert bot.generate("one thing") == "a"
    assert bot.generate("another thing") == "b"


def test_each_model_counts_its_own_calls():
    first = CannedModel("c1", ["a", "b"])
    second = CannedModel("c2", ["a", "b"])
    first.generate("x")
    first.generate("x")
    assert second.generate("x") == "a", "keep the counter on self, not in a shared place"


def test_describe_adds_the_number_of_replies():
    assert CannedModel("c1", ["Hi!", "Bye!"]).describe() == "model: c1 (2 replies)"


def test_describe_says_replies_even_for_one():
    assert CannedModel("solo", ["only"]).describe() == "model: solo (1 replies)"


def test_describe_builds_on_the_parents_describe(monkeypatch):
    monkeypatch.setattr(Model, "describe", lambda self: "X")
    assert CannedModel("c", ["a"]).describe() == "X (1 replies)", "use super().describe()"
