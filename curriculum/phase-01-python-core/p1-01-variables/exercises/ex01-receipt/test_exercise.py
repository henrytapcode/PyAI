import exercise


def test_quantity_is_three():
    assert exercise.quantity == 3


def test_quantity_is_an_int():
    assert type(exercise.quantity) is int


def test_total_is_price_times_quantity():
    assert exercise.total == 37.5


def test_label_text():
    assert exercise.label == "3 x notebook = 37.5"
