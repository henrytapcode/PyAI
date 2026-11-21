# Compare two isolated virtual environments and check required packages.
envs = {
    "chatbot": {"httpx": "0.25.0", "pydantic": "2.6.0"},
    "evals": {"httpx": "0.27.0", "pytest": "8.2.0"},
}

required = {"httpx": "0.27.0", "pydantic": "2.6.0"}

for name, installed in envs.items():
    missing = [pkg for pkg in required if pkg not in installed]
    mismatched = [
        f"{pkg} ({installed[pkg]} != {ver})"
        for pkg, ver in required.items()
        if pkg in installed and installed[pkg] != ver
    ]
    print(f"Env '{name}': missing={missing}, mismatched={mismatched}")
