from contextlib import contextmanager


@contextmanager
def temporary_setting(config, key, value):
    snapshot = dict(config)
    config[key] = value
    try:
        yield
    finally:
        config.clear()
        config.update(snapshot)
