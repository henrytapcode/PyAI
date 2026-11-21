import json

settings = {
    "python.defaultInterpreterPath": ".venv/bin/python",
    "editor.formatOnSave": True,
    "ruff.lineLength": 100,
    "[python]": {"editor.defaultFormatter": "charliermarsh.ruff"},
}

serialized = json.dumps(settings, indent=2)
print(serialized)

parsed = json.loads(serialized)
print("formatOnSave:", parsed["editor.formatOnSave"])
print("formatter:", parsed["[python]"]["editor.defaultFormatter"])
