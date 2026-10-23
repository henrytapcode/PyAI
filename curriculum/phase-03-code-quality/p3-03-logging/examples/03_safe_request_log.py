# Log a model request with useful fields, but without the secret key or the private text.
import logging
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s %(message)s | model=%(model)s tokens=%(tokens)s",
    force=True,
)
logger = logging.getLogger("app.api")


def mask_key(key):
    return "..." + key[-4:]


def log_request(model, api_key, prompt, tokens):
    logger.info(
        "request sent key=%s prompt_chars=%d",
        mask_key(api_key),
        len(prompt),
        extra={"model": model, "tokens": tokens},
    )


def log_failure(model, status):
    logger.error(
        "request failed status=%d",
        status,
        extra={"model": model, "tokens": 0},
    )


log_request("small", "sk-demo-1234567890", "Hello, my email is ana@example.com", 12)
log_failure("small", 429)
