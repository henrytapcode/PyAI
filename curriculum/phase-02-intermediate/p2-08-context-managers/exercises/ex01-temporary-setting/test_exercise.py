import pytest

from exercise import temporary_setting


def test_setting_has_the_new_value_inside_the_block():
    config = {"model": "small"}
    with temporary_setting(config, "model", "big"):
        assert config["model"] == "big", "set config[key] before the yield"


def test_old_value_comes_back_after_the_block():
    config = {"model": "small"}
    with temporary_setting(config, "model", "big"):
        pass
    assert config == {"model": "small"}


def test_changes_the_same_dict_it_was_given():
    config = {"temperature": 0.2}
    seen = []
    with temporary_setting(config, "temperature", 0.9):
        seen.append(config["temperature"])
    assert seen == [0.9]
    assert config["temperature"] == 0.2


def test_missing_key_exists_inside_and_is_removed_afterwards():
    config = {"model": "small"}
    with temporary_setting(config, "max_tokens", 50):
        assert config["max_tokens"] == 50
    assert config == {"model": "small"}, "a key that was missing before must be removed again"


def test_old_value_comes_back_when_the_block_raises():
    config = {"model": "small"}
    with pytest.raises(RuntimeError):
        with temporary_setting(config, "model", "big"):
            raise RuntimeError("model call failed")
    assert config == {"model": "small"}, "restore the value in a finally block"


def test_missing_key_is_removed_when_the_block_raises():
    config = {}
    with pytest.raises(ValueError):
        with temporary_setting(config, "debug", True):
            raise ValueError("boom")
    assert config == {}


def test_the_error_is_not_hidden():
    config = {"model": "small"}
    with pytest.raises(KeyError):
        with temporary_setting(config, "model", "big"):
            config["nope"]


def test_falsy_old_values_are_restored_too():
    config = {"temperature": 0, "stream": False, "stop": None}
    with temporary_setting(config, "temperature", 1.0):
        pass
    with temporary_setting(config, "stream", True):
        pass
    with temporary_setting(config, "stop", "END"):
        pass
    assert config == {"temperature": 0, "stream": False, "stop": None}


def test_nested_managers_restore_in_order():
    config = {"model": "small"}
    with temporary_setting(config, "model", "medium"):
        with temporary_setting(config, "model", "big"):
            assert config["model"] == "big"
        assert config["model"] == "medium", "restore what was there when this manager started"
    assert config["model"] == "small"


@pytest.mark.parametrize("key, value", [("model", "big"), ("top_p", 0.5), ("seed", 0)])
def test_works_for_different_keys_and_values(key, value):
    config = {"model": "small"}
    with temporary_setting(config, key, value):
        assert config[key] == value
    assert config == {"model": "small"}
