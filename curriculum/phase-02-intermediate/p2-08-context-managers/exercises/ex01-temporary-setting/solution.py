from contextlib import contextmanager


@contextmanager
def temporary_setting(config, key, value):
    """Set config[key] to value inside the with block, then restore it."""
    existed = key in config
    old = config.get(key)
    config[key] = value
    try:
        yield
    finally:
        if existed:
            config[key] = old
        else:
            del config[key]
