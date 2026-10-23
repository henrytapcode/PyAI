import pytest

from exercise import Message


def test_message_stores_role_and_content():
    msg = Message("user", "Hi there")
    assert msg.role == "user", "role must be the first field"
    assert msg.content == "Hi there", "content must be the second field"


def test_tags_are_empty_by_default():
    msg = Message("user", "Hi")
    assert msg.tags == [], "tags needs a default: field(default_factory=list)"


def test_tags_can_be_given():
    msg = Message("user", "Hi", ["question"])
    assert msg.tags == ["question"]


def test_each_message_has_its_own_tags_list():
    first = Message("user", "Hi")
    second = Message("user", "Hello")
    first.tags.append("greeting")
    assert second.tags == [], "use default_factory=list so the list is not shared"


def test_print_shows_all_fields(capsys):
    print(Message("user", "Hi there"))
    assert capsys.readouterr().out == "Message(role='user', content='Hi there', tags=[])\n"


def test_messages_with_same_data_are_equal():
    assert Message("user", "Hi") == Message("user", "Hi")
    assert Message("user", "Hi") != Message("assistant", "Hi")
    assert Message("user", "Hi", ["a"]) != Message("user", "Hi")


@pytest.mark.parametrize(
    "content, expected",
    [
        ("Hi there", 2),
        ("What is a dataclass ?", 5),
        ("one", 1),
        ("", 0),
    ],
)
def test_word_count(content, expected):
    assert Message("user", content).word_count() == expected


def test_to_dict_has_the_three_keys():
    msg = Message("assistant", "Hello", ["greeting"])
    assert msg.to_dict() == {"role": "assistant", "content": "Hello", "tags": ["greeting"]}


def test_to_dict_of_default_message():
    assert Message("user", "Hi there").to_dict() == {
        "role": "user",
        "content": "Hi there",
        "tags": [],
    }
