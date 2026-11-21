import pytest
from exercise import (
    CostBudget,
    FakeClock,
    Pricing,
    call_with_retry,
    run_budgeted_agent,
)
from pyai_llm import FakeLLM, RateLimitError, Usage


class StubRegistry:
    """Lightweight duck-typed registry with zero dependency on ex01."""

    def __init__(self, handler=None) -> None:
        self._handler = handler
        self.calls: list[tuple[str, dict, object]] = []

    def execute(self, name: str, args: dict, ctx) -> dict:
        self.calls.append((name, dict(args), ctx))
        if self._handler is not None:
            return self._handler(name, args, ctx)
        return {"ok": True, "status": "ok", "result": {"echo": args}, "error": None}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Fetch order details",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "string"}},
                "required": ["order_id"],
            },
        },
    }
]


def test_pricing_validation_rejects_negative_rates():
    Pricing(0.0, 0.0)
    with pytest.raises(ValueError):
        Pricing(-0.001, 0.002)
    with pytest.raises(ValueError):
        Pricing(0.001, -0.002)


def test_cost_budget_validation_and_limits():
    with pytest.raises(ValueError):
        CostBudget(0, 1.0)
    with pytest.raises(ValueError):
        CostBudget(100, 0.0)

    pricing = Pricing(input_per_1k=0.001, output_per_1k=0.002)
    budget = CostBudget(max_tokens=500, max_cost_usd=0.001)
    assert budget.total_tokens == 0
    assert budget.cost_usd == 0.0
    assert budget.check() is None

    cost1 = budget.record(Usage(prompt_tokens=200, completion_tokens=50, total_tokens=250), pricing)
    assert cost1 == 0.0003
    assert budget.total_tokens == 250
    assert budget.cost_usd == 0.0003
    assert budget.check() is None

    budget.record(Usage(prompt_tokens=200, completion_tokens=100, total_tokens=300), pricing)
    assert budget.total_tokens == 550
    assert budget.check() == "token_budget"


def test_cost_budget_detects_usd_cap_independently():
    pricing = Pricing(input_per_1k=0.01, output_per_1k=0.02)
    budget = CostBudget(max_tokens=10000, max_cost_usd=0.002)
    budget.record(Usage(prompt_tokens=200, completion_tokens=50, total_tokens=250), pricing)
    assert budget.cost_usd == 0.003
    assert budget.check() == "cost_budget"


def test_call_with_retry_succeeds_after_transient_errors():
    clock = FakeClock(start=10.0)
    state = {"n": 0}

    def flaky():
        state["n"] += 1
        if state["n"] == 1:
            raise RateLimitError("429")
        if state["n"] == 2:
            raise TimeoutError("504")
        return "done"

    res = call_with_retry(flaky, clock, max_retries=3, base_delay=0.5, idempotent=True)
    assert res == {
        "ok": True,
        "value": "done",
        "error": None,
        "attempts": 3,
        "wait_seconds": 1.5,
    }
    assert clock() == 11.5


def test_call_with_retry_exhausts_retries_and_does_not_retry_non_idempotent():
    clock = FakeClock()

    def always_rate_limited():
        raise RateLimitError("still busy")

    res = call_with_retry(
        always_rate_limited, clock, max_retries=2, base_delay=0.5, idempotent=True
    )
    assert res["ok"] is False
    assert res["value"] is None
    assert "still busy" in res["error"]
    assert res["attempts"] == 3
    assert res["wait_seconds"] == 1.5
    assert clock() == 1.5

    clock2 = FakeClock()
    res_non_idemp = call_with_retry(
        always_rate_limited, clock2, max_retries=3, base_delay=0.5, idempotent=False
    )
    assert res_non_idemp["ok"] is False
    assert res_non_idemp["attempts"] == 1
    assert res_non_idemp["wait_seconds"] == 0.0
    assert clock2() == 0.0


def test_call_with_retry_never_retries_non_transient_exception():
    clock = FakeClock()

    def bad_input():
        raise ValueError("invalid payload")

    res = call_with_retry(bad_input, clock, max_retries=3, base_delay=0.5, idempotent=True)
    assert res == {
        "ok": False,
        "value": None,
        "error": "invalid payload",
        "attempts": 1,
        "wait_seconds": 0.0,
    }
    assert clock() == 0.0


def test_run_budgeted_agent_tool_call_then_final_with_retries():
    clock = FakeClock()
    pricing = Pricing(input_per_1k=0.001, output_per_1k=0.002)
    budget = CostBudget(max_tokens=2000, max_cost_usd=0.05)
    registry = StubRegistry()
    client = FakeLLM(
        fail_times=2,
        script=[
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "ORD-1"}}]},
            "Order ORD-1 is shipped.",
        ],
    )

    out = run_budgeted_agent(
        task="Check order ORD-1",
        client=client,
        registry=registry,
        ctx={"request_id": "req-1"},
        clock=clock,
        pricing=pricing,
        budget=budget,
        tools=TOOLS,
        max_steps=5,
        max_retries=2,
    )
    assert out["stopped_reason"] == "final"
    assert out["answer"] == "Order ORD-1 is shipped."
    assert out["steps"] == 2
    assert out["retries"] == 2
    assert out["total_tokens"] > 0
    assert out["cost_usd"] > 0.0
    assert clock() == 1.5
    assert len(registry.calls) == 1
    assert registry.calls[0][0] == "lookup_order"
    assert registry.calls[0][1] == {"order_id": "ORD-1"}


def test_run_budgeted_agent_stops_on_rate_limit():
    clock = FakeClock()
    pricing = Pricing(0.001, 0.002)
    budget = CostBudget(max_tokens=1000, max_cost_usd=1.0)
    registry = StubRegistry()
    client = FakeLLM(fail_times=5, script=["never reached"])

    out = run_budgeted_agent(
        task="Hello",
        client=client,
        registry=registry,
        ctx=None,
        clock=clock,
        pricing=pricing,
        budget=budget,
        max_steps=3,
        max_retries=2,
    )
    assert out["stopped_reason"] == "rate_limit"
    assert out["answer"] is None
    assert out["steps"] == 0
    assert out["retries"] == 2
    assert registry.calls == []


def test_run_budgeted_agent_stops_on_token_and_cost_budgets():
    clock = FakeClock()
    pricing = Pricing(0.001, 0.002)

    # Pre-exhausted token budget stops before calling client.chat
    budget_pre = CostBudget(max_tokens=5, max_cost_usd=1.0)
    budget_pre.record(Usage(prompt_tokens=4, completion_tokens=2, total_tokens=6), pricing)
    client_pre = FakeLLM(fail_times=1, script=["should not run"])
    out_pre = run_budgeted_agent(
        task="Hello",
        client=client_pre,
        registry=StubRegistry(),
        ctx=None,
        clock=clock,
        pricing=pricing,
        budget=budget_pre,
    )
    assert out_pre["stopped_reason"] == "token_budget"
    assert out_pre["steps"] == 0
    assert out_pre["retries"] == 0

    # Post-step cost budget breach
    budget_cost = CostBudget(max_tokens=5000, max_cost_usd=0.000001)
    client_cost = FakeLLM(script=["Expensive reply"])
    out_cost = run_budgeted_agent(
        task="Hello",
        client=client_cost,
        registry=StubRegistry(),
        ctx=None,
        clock=clock,
        pricing=Pricing(1.0, 1.0),
        budget=budget_cost,
    )
    assert out_cost["stopped_reason"] == "cost_budget"
    assert out_cost["answer"] is None
    assert out_cost["steps"] == 1


def test_run_budgeted_agent_stops_on_max_steps_without_retrying_tools():
    clock = FakeClock()
    pricing = Pricing(0.001, 0.002)
    budget = CostBudget(max_tokens=5000, max_cost_usd=1.0)
    registry = StubRegistry(
        handler=lambda name, args, ctx: {
            "ok": False,
            "status": "tool_error",
            "result": None,
            "error": "boom",
        }
    )
    client = FakeLLM(
        script=[
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "1"}}]},
            {"tool_calls": [{"name": "lookup_order", "arguments": {"order_id": "2"}}]},
            "Final answer never reached",
        ]
    )

    out = run_budgeted_agent(
        task="Loop",
        client=client,
        registry=registry,
        ctx=None,
        clock=clock,
        pricing=pricing,
        budget=budget,
        tools=TOOLS,
        max_steps=2,
        max_retries=2,
    )
    assert out["stopped_reason"] == "max_steps"
    assert out["answer"] is None
    assert out["steps"] == 2
    assert len(registry.calls) == 2
