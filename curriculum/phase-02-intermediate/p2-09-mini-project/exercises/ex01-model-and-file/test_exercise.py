import json

import pytest

from exercise import Expense, check_expense, edit_expenses, load_expenses, save_expenses


def good():
    return Expense("2024-03-05", "food", 4.5, "pho")


def test_expense_note_defaults_to_empty_text():
    assert Expense("2024-03-05", "food", 4.5).note == ""


def test_expenses_with_equal_fields_are_equal():
    assert Expense("2024-03-05", "food", 4.5, "pho") == good()


def test_expense_is_frozen():
    with pytest.raises(AttributeError):
        good().amount = 10


def test_a_valid_expense_passes_the_check():
    assert check_expense(good()) is None
    assert check_expense(Expense("2024-12-31", "fun", 3)) is None, "whole numbers are fine"


@pytest.mark.parametrize(
    "date",
    ["2024-3-5", "24-03-05", "2024/03/05", "hello", "", "2024-03-0x", 20240305, None],
)
def test_bad_date_raises_value_error(date):
    with pytest.raises(ValueError):
        check_expense(Expense(date, "food", 4.5))


@pytest.mark.parametrize("category", ["", "   ", 5, None])
def test_empty_category_raises_value_error(category):
    with pytest.raises(ValueError):
        check_expense(Expense("2024-03-05", category, 4.5))


@pytest.mark.parametrize("amount", [0, -2.5, "12", None])
def test_amount_must_be_a_number_above_zero(amount):
    with pytest.raises(ValueError):
        check_expense(Expense("2024-03-05", "food", amount))


def test_save_writes_a_json_list_of_objects(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [good(), Expense("2024-03-06", "fun", 9.0)])
    assert json.loads(path.read_text(encoding="utf-8")) == [
        {"date": "2024-03-05", "category": "food", "amount": 4.5, "note": "pho"},
        {"date": "2024-03-06", "category": "fun", "amount": 9.0, "note": ""},
    ]


def test_save_then_load_gives_the_same_expenses(tmp_path):
    path = tmp_path / "e.json"
    expenses = [good(), Expense("2024-03-06", "fun", 9.0), Expense("2024-04-01", "food", 2, "phở")]
    save_expenses(path, expenses)
    assert load_expenses(path) == expenses


def test_an_empty_list_round_trips(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [])
    assert load_expenses(path) == []


def test_save_refuses_bad_data_and_writes_nothing(tmp_path):
    path = tmp_path / "e.json"
    with pytest.raises(ValueError):
        save_expenses(path, [good(), Expense("2024-03-06", "fun", -1)])
    assert not path.exists(), "check every expense before opening the file"


def test_save_refuses_bad_data_and_keeps_an_existing_file(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [good()])
    before = path.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        save_expenses(path, [Expense("2024-03-06", "fun", 9.0), Expense("bad date", "fun", 1)])
    assert path.read_text(encoding="utf-8") == before, "the old file must stay as it was"


def test_load_of_a_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_expenses(tmp_path / "nope.json")


@pytest.mark.parametrize(
    "text",
    [
        "this is not json",
        '{"date": "2024-03-05"}',
        "[5]",
        '[{"date": "2024-03-05", "category": "food"}]',
        '[{"date": "2024-03-05", "category": "food", "amount": 4.5, "tip": 1}]',
        '[{"date": "2024-03-05", "category": "food", "amount": -3, "note": ""}]',
        '[{"date": 20240305, "category": "food", "amount": 4.5, "note": ""}]',
        '[{"date": "2024-03-05", "category": 5, "amount": 4.5, "note": ""}]',
    ],
)
def test_load_of_bad_content_raises_value_error(tmp_path, text):
    path = tmp_path / "bad.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        load_expenses(path)


def test_edit_expenses_saves_the_changes_when_the_block_ends(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [good()])
    with edit_expenses(path) as expenses:
        assert expenses == [good()], "start from the expenses saved in the file"
        expenses.append(Expense("2024-03-06", "fun", 9.0))
    assert load_expenses(path) == [good(), Expense("2024-03-06", "fun", 9.0)]


def test_edit_expenses_starts_with_an_empty_list_for_a_missing_file(tmp_path):
    path = tmp_path / "new.json"
    with edit_expenses(path) as expenses:
        assert expenses == []
        expenses.append(good())
    assert load_expenses(path) == [good()]


def test_edit_expenses_leaves_the_file_unchanged_when_the_block_fails(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [good()])
    before = path.read_text(encoding="utf-8")
    with pytest.raises(RuntimeError):
        with edit_expenses(path) as expenses:
            expenses.append(Expense("2024-03-06", "fun", 9.0))
            raise RuntimeError("crash")
    assert path.read_text(encoding="utf-8") == before, "do not save when the block fails"


def test_edit_expenses_refuses_to_save_a_bad_expense(tmp_path):
    path = tmp_path / "e.json"
    save_expenses(path, [good()])
    before = path.read_text(encoding="utf-8")
    with pytest.raises(ValueError):
        with edit_expenses(path) as expenses:
            expenses.append(Expense("2024-03-06", "fun", -5))
    assert path.read_text(encoding="utf-8") == before
