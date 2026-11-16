# Structured JSON request logging with FakeLLM, cache hits, and simulated error handling.

import json
import logging
import sys

from pyai_llm import FakeLLM, RateLimitError

PRICE_IN_PER_1K = 0.0005
PRICE_OUT_PER_1K = 0.0015


class FakeClock:
    def __init__(self, start_ms: float = 0.0) -> None:
        self.now_ms = start_ms

    def advance(self, ms: float) -> None:
        self.now_ms += ms


def main() -> None:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(message)s",
        force=True,
    )
    logger = logging.getLogger("app.metrics")

    client = FakeLLM(fail_times=1)
    clock = FakeClock()
    cache: dict[str, str] = {}
    logged = 0

    requests = [
        ("req-01", "/ask", "What is RAG?"),
        ("req-02", "/ask", "What is RAG?"),
        ("req-03", "/ask", "What is a token?"),
        ("req-04", "/ask", "What is temperature?"),
        ("req-05", "/ask", "What is RAG?"),
        ("req-06", "/summarize", "Summarize embeddings."),
        ("req-07", "/ask", "What is a token?"),
        ("req-08", "/ask", "What is hallucination?"),
    ]

    for req_id, route, question in requests:
        start_ms = clock.now_ms
        if question in cache:
            clock.advance(2.0)
            prompt_tokens = 0
            completion_tokens = 0
            cache_hit = True
            status = "ok"
        else:
            cache_hit = False
            try:
                resp = client.chat([{"role": "user", "content": question}], temperature=0.0)
                clock.advance(200.0 + 3.0 * resp.usage.completion_tokens)
                prompt_tokens = resp.usage.prompt_tokens
                completion_tokens = resp.usage.completion_tokens
                cache[question] = resp.content or ""
                status = "ok"
            except RateLimitError:
                clock.advance(150.0)
                prompt_tokens = 0
                completion_tokens = 0
                status = "error"

        cost = (prompt_tokens / 1000) * PRICE_IN_PER_1K + (completion_tokens / 1000) * PRICE_OUT_PER_1K
        record = {
            "request_id": req_id,
            "route": route,
            "model": "fake-mini",
            "latency_ms": round(clock.now_ms - start_ms, 1),
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": round(cost, 6),
            "cache_hit": cache_hit,
            "status": status,
        }
        logger.info(json.dumps(record, sort_keys=True))
        logged += 1

    print("logged_lines:", logged)


if __name__ == "__main__":
    main()
