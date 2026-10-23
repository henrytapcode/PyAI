from contextlib import contextmanager


@contextmanager
def temporary_setting(config, key, value):
    """Set config[key] to value inside the with block, then restore it.

    Example:
        config = {"model": "small"}
        with temporary_setting(config, "model", "big"):
            ...  # config["model"] is "big" here
        # config["model"] is "small" again here
    """
    # TODO 1: remember whether key is in config, and its old value
    # TODO 2: set config[key] = value
    # TODO 3: yield inside try, and restore in finally
    # (if key was missing before, remove it again)
    yield
