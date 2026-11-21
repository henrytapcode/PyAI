# Parse a pyproject.toml string with Python's built-in tomllib.
import tomllib

pyproject_toml = """
[project]
name = "rag-assistant"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.27.0",
    "pydantic==2.7.1",
    "pyyaml",
]
"""

data = tomllib.loads(pyproject_toml)
project = data["project"]

print("Project:", project["name"])
print("Python: ", project["requires-python"])
print("Dependencies:")
for dep in project["dependencies"]:
    print(" -", dep)
