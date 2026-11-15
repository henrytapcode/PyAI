# Safe toolbox: allowlist, required-arg validation, extra-arg filtering, and error strings.
import json

ORDERS = {
    "1042": {"status": "delayed", "carrier": "FastShip", "total": 50.0, "days_late": 4},
    "1043": {"status": "shipped", "carrier": "FastShip", "total": 35.0, "days_late": 0},
}
SHIPMENTS = {("FastShip", "1042"): "hub delay (+4d)"}
REFUNDS = {}


def lookup_order(order_id: str) -> dict:
    if order_id not in ORDERS:
        return {"error": f"order {order_id} not found"}
    o = ORDERS[order_id]
    return {"status": o["status"], "total": o["total"], "late": o["days_late"]}


def track_shipment(carrier: str, order_id: str) -> str:
    return SHIPMENTS.get((carrier, order_id), "error: no tracking")


def check_refund_policy(days_late: int) -> str:
    if days_late < 0:
        raise ValueError("days_late must be >= 0")
    return "eligible: max 20% refund" if days_late >= 3 else "not eligible"


def issue_refund(order_id: str, amount: float) -> str:
    REFUNDS[order_id] = amount
    return f"refunded ${amount:.2f} for {order_id}"


REGISTRY = {
    "lookup_order": (
        lookup_order,
        {"name": "lookup_order", "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
        False,
    ),
    "track_shipment": (
        track_shipment,
        {"name": "track_shipment", "parameters": {"type": "object", "properties": {"carrier": {"type": "string"}, "order_id": {"type": "string"}}, "required": ["carrier", "order_id"]}},
        False,
    ),
    "check_refund_policy": (
        check_refund_policy,
        {"name": "check_refund_policy", "parameters": {"type": "object", "properties": {"days_late": {"type": "integer"}}, "required": ["days_late"]}},
        False,
    ),
    "issue_refund": (
        issue_refund,
        {"name": "issue_refund", "parameters": {"type": "object", "properties": {"order_id": {"type": "string"}, "amount": {"type": "number"}}, "required": ["order_id", "amount"]}},
        True,
    ),
}


def invoke(name: str, args: dict) -> str:
    if name not in REGISTRY:
        return f"error: unknown tool {name}"
    fn, schema, _ = REGISTRY[name]
    params = schema["parameters"]
    props = params.get("properties", {})
    for req in params.get("required", []):
        if req not in args or args[req] in (None, ""):
            return f"error: missing {req}"
    clean = {k: v for k, v in args.items() if k in props}
    try:
        out = fn(**clean)
    except Exception as err:
        return f"error: {err}"
    return json.dumps(out) if isinstance(out, dict) else str(out)


cases = [
    ("ok_dict", "lookup_order", {"order_id": "1042", "extra": 1}),
    ("ok_str ", "track_shipment", {"carrier": "FastShip", "order_id": "1042"}),
    ("unknown", "delete_orders", {"order_id": "1042"}),
    ("missing", "track_shipment", {"carrier": "FastShip"}),
    ("raised ", "check_refund_policy", {"days_late": -2}),
]
for label, tool_name, tool_args in cases:
    print(f"{label}: {invoke(tool_name, tool_args)}")
