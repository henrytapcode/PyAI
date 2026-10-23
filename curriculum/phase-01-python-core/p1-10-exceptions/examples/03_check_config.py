# Validate settings early: raise clear errors, catch them in one place.
def check_config(config):
    if "model" not in config:
        raise ValueError("config needs a 'model' key")
    temperature = config.get("temperature", 0.7)
    if temperature < 0 or temperature > 2:
        raise ValueError(f"temperature must be between 0 and 2, got {temperature}")
    return config["model"], temperature


configs = [
    {"model": "small", "temperature": 0.2},
    {"temperature": 0.5},
    {"model": "large", "temperature": 5},
]

for config in configs:
    try:
        model, temperature = check_config(config)
    except ValueError as err:
        print("config rejected:", err)
    else:
        print(f"config ok: {model} at {temperature}")
    finally:
        print("-- checked one config")
