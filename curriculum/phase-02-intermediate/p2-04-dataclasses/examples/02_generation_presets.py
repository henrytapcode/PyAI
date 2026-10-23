# Read-only generation settings with sensible defaults, and a few named presets.
from dataclasses import dataclass


@dataclass(frozen=True)
class GenerationConfig:
    model: str
    temperature: float = 0.7
    max_tokens: int = 256

    def is_deterministic(self):
        return self.temperature == 0

    def describe(self):
        if self.is_deterministic():
            mode = "deterministic"
        else:
            mode = "creative"
        return f"{self.model}: {mode}, up to {self.max_tokens} tokens"


presets = {
    "default": GenerationConfig("small"),
    "precise": GenerationConfig("large", temperature=0.0, max_tokens=1024),
    "brainstorm": GenerationConfig("small", temperature=1.2),
}

for name in presets:
    print(name, "->", presets[name].describe())

config = presets["default"]
try:
    config.temperature = 2.0
except AttributeError:
    print("presets are read-only")
print(config)

lower = GenerationConfig(config.model, temperature=0.2, max_tokens=config.max_tokens)
print(lower)
print(lower == config)
