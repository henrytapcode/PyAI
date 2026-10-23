# Build model settings from defaults plus overrides, without sharing state between calls.
DEFAULTS = {"model": "small", "temperature": 0.2, "max_tokens": 256}


def build_settings(overrides: dict[str, float | str] | None = None) -> dict[str, float | str]:
    settings = dict(DEFAULTS)
    if overrides is not None:
        settings.update(overrides)
    return settings


creative = build_settings({"temperature": 0.9})
plain = build_settings()
print("creative:", creative)
print("plain:", plain)
print("defaults untouched:", DEFAULTS == {"model": "small", "temperature": 0.2, "max_tokens": 256})
print("separate dicts:", creative is not plain)
