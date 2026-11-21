_MISSING = object()


def three_way_merge(
    base: dict[str, str],
    main: dict[str, str],
    feature: dict[str, str],
) -> dict:
    merged: dict[str, str] = {}
    conflicts: list[str] = []

    for path in sorted(base.keys() | main.keys() | feature.keys()):
        b_val = base.get(path, _MISSING)
        m_val = main.get(path, _MISSING)
        f_val = feature.get(path, _MISSING)

        if m_val == f_val:
            if m_val is not _MISSING:
                merged[path] = str(m_val)
        elif m_val == b_val:
            if f_val is not _MISSING:
                merged[path] = str(f_val)
        elif f_val == b_val:
            if m_val is not _MISSING:
                merged[path] = str(m_val)
        else:
            conflicts.append(path)
            if m_val is not _MISSING:
                merged[path] = str(m_val)

    return {"merged": merged, "conflicts": conflicts}


def is_valid_commit_msg(msg: str) -> bool:
    subject = msg.split("\n", 1)[0].strip()
    if not subject or len(subject) > 72 or subject.endswith("."):
        return False
    return subject[0].isascii() and subject[0].isalpha()
