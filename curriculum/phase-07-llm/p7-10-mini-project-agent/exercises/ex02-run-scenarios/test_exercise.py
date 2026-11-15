import copy
import pytest
from exercise import run_scenario, summarize
from pyai_llm import FakeLLM


class MiniToolbox:
    """Minimal self-contained toolbox used solely by ex02 tests."""

    def __init__(self, refund_counter: dict | None = None) -> None:
        self._counter = refund_counter if refund_counter is not None else {"refunds": 0}
        self._schemas = [
            {
                "name": "lookup_order",
                "description": "lookup order",
                "parameters": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"],
                },
            },
            {
                "name": "check_policy",
                "description": "check policy",
                "parameters": {
                    "type": "object",
                    "properties": {"days": {"type": "integer"}},
                    "required": ["days"],
                },
            },
            {
                "name": "issue_refund",
                "description": "issue refund",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string"},
                        "amount": {"type": "number"},
                    },
                    "required": ["order_id", "amount"],
                },
            },
        ]

    def schemas(self) -> list[dict]:
        return [dict(s) for s in self._schemas]

    def is_side_effect(self, name: str) -> bool:
        return name == "issue_refund"

    def call(self, name: str, args: dict) -> str:
        if name == "lookup_order":
            return f"order {args.get('order_id')} delayed 4d"
        if name == "check_policy":
            return "eligible 20%"
        if name == "issue_refund":
            self._counter["refunds"] += 1
            return f"refunded {args.get('amount')} for {args.get('order_id')}"
        return f"error: unknown tool {name}"


def _make_client(script):
    return FakeLLM(script=script)


def test_happy_path_passes_with_exact_trajectory():
    scenario = {
        "name": "happy",
        "task": "Check order 1042",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_policy", "arguments": {"days": 4}}]},
            "Order 1042 is eligible for a 20% refund.",
        ],
        "approve": None,
        "expect": {
            "stopped_reason": "final",
            "tools": ["lookup_order", "check_policy"],
            "answer_contains": "20%",
        },
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res == {
        "name": "happy",
        "passed": True,
        "stopped_reason": "final",
        "tools": ["lookup_order", "check_policy"],
        "reasons": [],
    }


def test_wrong_trajectory_order_fails_with_tools_reason():
    scenario = {
        "name": "wrong_order",
        "task": "Check order 1042",
        "script": [
            {"tool_calls": [{"name": "check_policy", "arguments": {"days": 4}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            "Eligible 20%.",
        ],
        "approve": None,
        "expect": {
            "stopped_reason": "final",
            "tools": ["lookup_order", "check_policy"],
            "answer_contains": "20%",
        },
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res["passed"] is False
    assert res["tools"] == ["check_policy", "lookup_order"]
    assert res["reasons"] == ["tools"]


def test_rejected_approval_stops_without_executing_side_effect():
    counter = {"refunds": 0}
    scenario = {
        "name": "reject_refund",
        "task": "Refund 1042",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {
                "tool_calls": [
                    {"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 50.0}}
                ]
            },
        ],
        "approve": lambda name, args: False,
        "expect": {
            "stopped_reason": "rejected",
            "tools": ["lookup_order"],
            "answer_contains": "",
        },
    }
    res = run_scenario(scenario, MiniToolbox(counter), _make_client)
    assert res["passed"] is True
    assert res["stopped_reason"] == "rejected"
    assert res["tools"] == ["lookup_order"]
    assert counter["refunds"] == 0, "side-effect tool must NOT run when approve returns False"


def test_missing_approve_callback_also_blocks_side_effect():
    counter = {"refunds": 0}
    scenario = {
        "name": "no_callback",
        "task": "Refund 1042",
        "script": [
            {
                "tool_calls": [
                    {"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 10.0}}
                ]
            },
        ],
        "expect": {"stopped_reason": "needs_approval", "tools": [], "answer_contains": ""},
    }
    res = run_scenario(scenario, MiniToolbox(counter), _make_client)
    assert res["passed"] is True
    assert res["stopped_reason"] == "needs_approval"
    assert counter["refunds"] == 0


def test_approved_side_effect_executes_and_appears_in_tools():
    counter = {"refunds": 0}
    scenario = {
        "name": "approve_refund",
        "task": "Refund 1042",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {
                "tool_calls": [
                    {"name": "issue_refund", "arguments": {"order_id": "1042", "amount": 10.0}}
                ]
            },
            "Refunded $10.00.",
        ],
        "approve": lambda name, args: name == "issue_refund" and args["amount"] <= 10.0,
        "expect": {
            "stopped_reason": "final",
            "tools": ["lookup_order", "issue_refund"],
            "answer_contains": "$10.00",
        },
    }
    res = run_scenario(scenario, MiniToolbox(counter), _make_client)
    assert res["passed"] is True
    assert res["tools"] == ["lookup_order", "issue_refund"]
    assert counter["refunds"] == 1


def test_repeat_guard_stops_on_identical_consecutive_call():
    scenario = {
        "name": "repeat_case",
        "task": "Check 1042",
        "max_steps": 5,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        ],
        "expect": {"stopped_reason": "repeat", "tools": ["lookup_order"], "answer_contains": ""},
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res["passed"] is True
    assert res["stopped_reason"] == "repeat"


def test_max_steps_stops_when_limit_reached():
    scenario = {
        "name": "cap_case",
        "task": "Check 1042",
        "max_steps": 2,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_policy", "arguments": {"days": 4}}]},
            "Done.",
        ],
        "expect": {
            "stopped_reason": "max_steps",
            "tools": ["lookup_order", "check_policy"],
            "answer_contains": "",
        },
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res["passed"] is True
    assert res["stopped_reason"] == "max_steps"


def test_budget_guard_stops_when_token_budget_exceeded():
    scenario = {
        "name": "budget_case",
        "task": "Check 1042",
        "token_budget": 10,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            "Done.",
        ],
        "expect": {"stopped_reason": "budget", "tools": [], "answer_contains": ""},
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res["passed"] is True
    assert res["stopped_reason"] == "budget"


def test_missing_answer_and_fixed_reason_order():
    scenario = {
        "name": "all_wrong",
        "task": "Check 1042",
        "max_steps": 1,
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
        ],
        "expect": {
            "stopped_reason": "final",
            "tools": ["check_policy"],
            "answer_contains": "refunded",
        },
    }
    res = run_scenario(scenario, MiniToolbox(), _make_client)
    assert res["passed"] is False
    assert res["reasons"] == ["stopped_reason", "tools", "answer"]


def test_fresh_client_per_scenario_and_no_input_mutation():
    calls = []

    def spy_make_client(script):
        calls.append(list(script))
        return FakeLLM(script=script)

    scenario_a = {
        "name": "s_a",
        "task": "A",
        "script": ["Answer A"],
        "expect": {"stopped_reason": "final", "tools": [], "answer_contains": "A"},
    }
    scenario_b = {
        "name": "s_b",
        "task": "B",
        "script": ["Answer B"],
        "expect": {"stopped_reason": "final", "tools": [], "answer_contains": "B"},
    }
    snap_a = {
        "name": "s_a",
        "task": "A",
        "script": ["Answer A"],
        "expect": {"stopped_reason": "final", "tools": [], "answer_contains": "A"},
    }
    ra = run_scenario(scenario_a, MiniToolbox(), spy_make_client)
    rb = run_scenario(scenario_b, MiniToolbox(), spy_make_client)
    assert ra["passed"] is True and rb["passed"] is True
    assert len(calls) == 2
    assert scenario_a == snap_a


@pytest.mark.parametrize(
    ("results", "expected"),
    [
        (
            [
                {"name": "s1", "passed": True, "reasons": []},
                {"name": "s2", "passed": True, "reasons": []},
            ],
            ["passed: 2/2", "all passed"],
        ),
        (
            [
                {"name": "s1", "passed": True, "reasons": []},
                {"name": "s2", "passed": False, "reasons": ["stopped_reason", "tools"]},
                {"name": "s3", "passed": False, "reasons": ["answer"]},
            ],
            [
                "passed: 1/3",
                "FAIL s2: stopped_reason, tools",
                "FAIL s3: answer",
            ],
        ),
    ],
)
def test_summarize_formats_passing_and_failing_runs(results, expected):
    assert summarize(results) == expected


class _SpyClient:
    def __init__(self, inner) -> None:
        self._inner = inner
        self.calls: list[list[dict]] = []

    def chat(self, messages, tools=None):
        self.calls.append(copy.deepcopy(messages))
        return self._inner.chat(messages, tools=tools)


def test_appends_assistant_and_tool_messages_to_history():
    spy_holder: list[_SpyClient] = []

    def make_spy(script):
        client = _SpyClient(FakeLLM(script=script))
        spy_holder.append(client)
        return client

    scenario = {
        "name": "history_check",
        "task": "Check order 1042",
        "script": [
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1042"}}]},
            {"tool_calls": [{"name": "check_policy", "arguments": {"days": 4}}]},
            "Order 1042 is eligible for 20% refund.",
        ],
        "approve": None,
        "expect": {
            "stopped_reason": "final",
            "tools": ["lookup_order", "check_policy"],
            "answer_contains": "20%",
        },
    }
    res = run_scenario(scenario, MiniToolbox(), make_spy)
    assert res["passed"] is True
    assert len(spy_holder) == 1
    calls = spy_holder[0].calls
    assert len(calls) == 3

    second_msgs = calls[1]
    assert len(second_msgs) == 3
    assert second_msgs[1]["role"] == "assistant"
    assert second_msgs[1]["tool_calls"][0]["name"] == "lookup_order"
    tc_id = second_msgs[1]["tool_calls"][0]["id"]
    assert second_msgs[2]["role"] == "tool"
    assert second_msgs[2]["tool_call_id"] == tc_id
    assert second_msgs[2]["content"] == "order 1042 delayed 4d"
