# Call a fake model with retries and log every attempt as key=value fields.
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s %(name)s %(message)s",
    force=True,
)
logger = logging.getLogger("app.llm")

replies = ["TIMEOUT", "Paris is the capital of France."]  # the first call fails
ticks = iter([0.0, 0.5, 1.3])  # a fake clock: start, start, end


def fake_model(prompt, attempt):
    reply = replies[attempt - 1]
    if reply == "TIMEOUT":
        raise TimeoutError("no answer in time")
    return reply


def call_model(model, prompt, max_attempts=3):
    for attempt in range(1, max_attempts + 1):
        start = next(ticks)
        try:
            reply = fake_model(prompt, attempt)
        except TimeoutError as err:
            logger.warning("llm_retry model=%s attempt=%d reason=%s", model, attempt, err)
            continue
        latency = next(ticks) - start
        logger.info(
            "llm_call model=%s attempt=%d latency=%.2fs chars=%d",
            model, attempt, latency, len(reply),
        )
        return reply
    logger.error("llm_failed model=%s attempts=%d", model, max_attempts)
    return None


answer = call_model("small", "What is the capital of France?")
print(answer)
