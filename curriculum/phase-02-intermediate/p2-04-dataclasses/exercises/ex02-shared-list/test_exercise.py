import pytest

from exercise import Chat, GenerationConfig


def test_new_chat_starts_empty():
    chat = Chat("demo")
    assert chat.title == "demo"
    assert chat.messages == [], "a new chat starts with an empty list"
    assert chat.count() == 0


def test_add_stores_the_text():
    chat = Chat("demo")
    chat.add("Hi")
    chat.add("Hello")
    assert chat.messages == ["Hi", "Hello"]
    assert chat.count() == 2


def test_chats_do_not_share_their_messages():
    first = Chat("first")
    second = Chat("second")
    first.add("Hi")
    assert second.messages == [], "every chat needs its own list: use default_factory"
    assert second.count() == 0


def test_messages_can_be_given_when_creating_a_chat():
    chat = Chat("demo", ["a", "b"])
    assert chat.count() == 2


def test_config_defaults():
    config = GenerationConfig("small")
    assert config.model == "small"
    assert config.temperature == pytest.approx(0.7)
    assert config.max_tokens == 256


def test_config_accepts_temperature_by_keyword():
    config = GenerationConfig("small", temperature=0.2)
    assert config.temperature == pytest.approx(0.2), "temperature needs an annotation to be a field"
    assert config.max_tokens == 256


def test_config_accepts_values_by_position():
    config = GenerationConfig("large", 0.0, 1024)
    assert (config.model, config.temperature, config.max_tokens) == ("large", 0.0, 1024)


def test_config_prints_all_fields(capsys):
    print(GenerationConfig("small", temperature=0.2))
    expected = "GenerationConfig(model='small', temperature=0.2, max_tokens=256)\n"
    assert capsys.readouterr().out == expected


def test_config_is_read_only():
    config = GenerationConfig("small")
    with pytest.raises(AttributeError):
        config.max_tokens = 1
    assert config.max_tokens == 256


def test_config_temperature_is_read_only_too():
    config = GenerationConfig("small")
    with pytest.raises(AttributeError):
        config.temperature = 2.0


def test_configs_with_same_values_are_equal():
    assert GenerationConfig("small") == GenerationConfig("small", 0.7, 256)
