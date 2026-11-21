base = {"app.py": "v1", "config.py": "port=8000"}
main = {"app.py": "v1", "config.py": "port=9000"}
feature = {"app.py": "v2", "config.py": "port=9001"}

merged = {}
conflicts = []

for name in sorted(base | main | feature):
    b_val = base.get(name)
    m_val = main.get(name)
    f_val = feature.get(name)

    if m_val == f_val:
        if m_val is not None:
            merged[name] = m_val
    elif m_val == b_val:
        if f_val is not None:
            merged[name] = f_val
    elif f_val == b_val:
        if m_val is not None:
            merged[name] = m_val
    else:
        conflicts.append(name)
        if m_val is not None:
            merged[name] = m_val

print("Merged:", merged)
print("Conflicts:", conflicts)
