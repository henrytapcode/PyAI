class TemporarySetting:
    def __init__(self, config, key, value):
        self.config = config
        self.key = key
        self.value = value
        self.existed = False
        self.old = None

    def __enter__(self):
        self.existed = self.key in self.config
        self.old = self.config.get(self.key)
        self.config[self.key] = self.value
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.existed:
            self.config[self.key] = self.old
        else:
            del self.config[self.key]
        return False


def temporary_setting(config, key, value):
    return TemporarySetting(config, key, value)
