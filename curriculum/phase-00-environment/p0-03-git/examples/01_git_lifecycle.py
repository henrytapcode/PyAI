committed = {"README.md": "# Demo"}
staged = dict(committed)
working = {"README.md": "# Demo\nSetup", "app.py": "print('hi')"}

untracked = sorted(p for p in working if p not in staged and p not in committed)
modified = sorted(p for p in staged if p in working and working[p] != staged[p])
print("Before add -> untracked:", untracked, "modified:", modified)

staged["README.md"] = working["README.md"]
staged["app.py"] = working["app.py"]
print("Staged keys:", sorted(staged))

committed = dict(staged)
print("Committed count:", len(committed))
