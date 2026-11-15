def run_scenario(scenario: dict, toolbox, make_client) -> dict:
    """Execute one scripted agent scenario with safety guards and compare to expect.

    Example:
        run_scenario(scenario, toolbox, lambda sc: FakeLLM(script=sc))
        -> {"name": "happy", "passed": True, "stopped_reason": "final",
            "tools": [...], "reasons": []}
    """
    # TODO: create fresh client, run bounded loop with budget/final/repeat/approval,
    # dispatch via toolbox.call, and score against scenario["expect"].
    return None


def summarize(results: list[dict]) -> list[str]:
    """Format scenario pass counts, per-failure reasons, and all-passed status.

    Example:
        summarize([{"name": "s1", "passed": True, "reasons": []}])
        -> ["passed: 1/1", "all passed"]
    """
    # TODO: build ["passed: X/Y", ...FAIL lines or "all passed"].
    return None
