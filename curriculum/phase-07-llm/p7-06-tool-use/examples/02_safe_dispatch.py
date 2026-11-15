# Safe dispatch: validate tool names, required args, types, and runtime exceptions.
import json

from pyai_llm import ToolCall

WEATHER = {"Hanoi": "31C and sunny", "Hue": "28C and cloudy"}


def get_weather(city: str, unit: str = "C") -> dict:
    if city not in WEATHER:
        raise ValueError(f"city not found: {city}")
    return {"city": city, "unit": unit, "forecast": WEATHER[city]}


def add_tax(price: float, rate: float = 0.1) -> str:
    if not isinstance(price, (int, float)) or isinstance(price, bool):
        raise TypeError("price must be a number")
    return f"{round(price * (1 + rate), 2)}"


REGISTRY = {"get_weather": get_weather, "add_tax": add_tax}
REQUIRED = {"get_weather": ["city"], "add_tax": ["price"]}


def dispatch(call: ToolCall, registry: dict, required_map: dict) -> str:
    if call.name not in registry:
        return f"error: unknown tool {call.name}"
    req = required_map.get(call.name, [])
    args = dict(call.arguments)
    for key in req:
        if key not in args or args[key] in ("", None):
            return f"error: missing required argument {key}"
    clean = {k: v for k, v in args.items() if k in req or v not in ("", None)}
    try:
        out = registry[call.name](**clean)
    except Exception as err:
        return f"error: {type(err).__name__}: {err}"
    return json.dumps(out) if isinstance(out, dict) else str(out)


test_calls = [
    ToolCall(id="call_1", name="get_weather", arguments={"city": "Hanoi", "unit": ""}),
    ToolCall(id="call_2", name="drop_table", arguments={"table": "orders"}),
    ToolCall(id="call_3", name="get_weather", arguments={"unit": "C"}),
    ToolCall(id="call_4", name="add_tax", arguments={"price": "free"}),
    ToolCall(id="call_5", name="get_weather", arguments={"city": "Atlantis"}),
]

for tc in test_calls:
    print(f"{tc.id} ({tc.name}) -> {dispatch(tc, REGISTRY, REQUIRED)}")
