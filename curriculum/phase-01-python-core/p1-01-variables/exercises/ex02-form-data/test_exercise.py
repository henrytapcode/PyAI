import exercise


def test_inputs_unchanged():
    assert exercise.age_text == "29"
    assert exercise.height_text == "1.72"


def test_age_is_int_29():
    assert type(exercise.age) is int
    assert exercise.age == 29


def test_height_is_float():
    assert type(exercise.height) is float
    assert exercise.height == 1.72


def test_age_next_year():
    assert exercise.age_next_year == 30


def test_summary_text():
    assert exercise.summary == "Age 29, height 1.72m"
