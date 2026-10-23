# Stage 1: model an LLM API call as a frozen dataclass, check it, and keep a JSON call log.
import json
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class ApiCall:
    day: str
    model: str
    tokens: int
    cost: float


def check_call(call: ApiCall) -> None:
    if not call.model.strip():
        raise ValueError("model must not be empty")
    if call.tokens <= 0:
        raise ValueError(f"tokens must be positive, got {call.tokens}")
    if call.cost < 0:
        raise ValueError(f"cost must not be negative, got {call.cost}")


def save_calls(path: Path, calls: list[ApiCall]) -> None:
    for call in calls:
        check_call(call)
    path.write_text(json.dumps([asdict(c) for c in calls]), encoding="utf-8")


def load_calls(path: Path) -> list[ApiCall]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return [ApiCall(**record) for record in records]


calls = [
    ApiCall("2024-05-01", "small", 1200, 0.002),
    ApiCall("2024-05-01", "large", 800, 0.04),
    ApiCall("2024-05-02", "small", 300, 0.0005),
]

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "calls.json"
    save_calls(path, calls)
    loaded = load_calls(path)
    print("saved", len(calls), "loaded", len(loaded))
    print("same data:", loaded == calls)

    bad = [ApiCall("2024-05-03", "small", 0, 0.0)]
    try:
        save_calls(path, bad)
    except ValueError as err:
        print("refused:", err)
    print("file still has", len(load_calls(path)), "calls")

try:
    calls[0].tokens = 5
except AttributeError:
    print("a saved call cannot be edited")
