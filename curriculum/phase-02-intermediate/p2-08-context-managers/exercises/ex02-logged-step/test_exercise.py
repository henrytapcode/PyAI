import pytest

from exercise import logged_step


def test_logs_start_and_end_around_the_block():
    log = []
    with logged_step(log, "embed"):
        pass
    assert log == ["start embed", "end embed"]


def test_start_is_logged_before_the_body_runs():
    log = []
    seen = []
    with logged_step(log, "embed"):
        seen.append(list(log))
    assert seen == [["start embed"]], "the start message must be added before yield"


def test_end_is_not_logged_until_the_body_is_done():
    log = []
    with logged_step(log, "embed"):
        log.append("work")
    assert log == ["start embed", "work", "end embed"]


def test_as_gives_the_step_name():
    log = []
    with logged_step(log, "chunk") as step:
        assert step == "chunk", "yield the name so that 'as' receives it"


def test_end_is_logged_when_the_body_raises():
    log = []
    with pytest.raises(ValueError):
        with logged_step(log, "embed"):
            raise ValueError("boom")
    assert log == ["start embed", "end embed"], "the end message belongs in finally"


def test_the_error_is_not_hidden():
    log = []
    with pytest.raises(RuntimeError, match="api down"):
        with logged_step(log, "call"):
            raise RuntimeError("api down")


def test_two_steps_in_a_row_use_their_own_names():
    log = []
    with logged_step(log, "load"):
        pass
    with logged_step(log, "embed"):
        pass
    assert log == ["start load", "end load", "start embed", "end embed"]


def test_nested_steps_end_in_reverse_order():
    log = []
    with logged_step(log, "outer"):
        with logged_step(log, "inner"):
            pass
    assert log == ["start outer", "start inner", "end inner", "end outer"]


@pytest.mark.parametrize("name", ["a", "load data", "step 2"])
def test_works_with_any_name(name):
    log = []
    with logged_step(log, name):
        pass
    assert log == ["start " + name, "end " + name]
