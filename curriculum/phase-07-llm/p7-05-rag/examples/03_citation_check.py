# Detect invalid out-of-range citations and missing citations from a scripted LLM.
import re

from pyai_llm import FakeLLM


def check_citations(answer: str, n_chunks: int) -> dict:
    refs = [int(n) for n in re.findall(r"\[(\d+)\]", answer)]
    invalid = [r for r in refs if r < 1 or r > n_chunks]
    valid = [r for r in refs if 1 <= r <= n_chunks]
    return {
        "valid": valid,
        "invalid": invalid,
        "missing": len(refs) == 0,
    }


hits = [
    {"source": "refunds.md", "text": "Refunds are issued within 30 days."},
    {"source": "shipping.md", "text": "Standard shipping delivers in five days."},
]
client = FakeLLM(
    script=[
        "Refunds take 30 days. [1]",
        "Refunds take 30 days and warranty is 2 years. [3]",
        "Refunds are usually processed quickly.",
    ]
)
for label in ["grounded", "hallucinated_ref", "uncited"]:
    ans = client.chat([{"role": "user", "content": "Refund policy?"}]).content or ""
    report = check_citations(ans, len(hits))
    print(label, "->", ans)
    print("  check:", report)
