def three_way_merge(
    base: dict[str, str],
    main: dict[str, str],
    feature: dict[str, str],
) -> dict:
    merged: dict[str, str] = {}
    conflicts: list[str] = []

    for path in sorted(set(base) | set(main) | set(feature)):
        in_b, in_m, in_f = path in base, path in main, path in feature
        b_val = base.get(path)
        m_val = main.get(path)
        f_val = feature.get(path)

        if (in_m, m_val) == (in_f, f_val):
            if in_m:
                merged[path] = main[path]
        elif (in_m, m_val) == (in_b, b_val):
            if in_f:
                merged[path] = feature[path]
        elif (in_f, f_val) == (in_b, b_val):
            if in_m:
                merged[path] = main[path]
        else:
            conflicts.append(path)
            if in_m:
                merged[path] = main[path]

    return {"merged": merged, "conflicts": conflicts}


def is_valid_commit_msg(msg: str) -> bool:
    first_line = msg.splitlines()[0].strip() if msg else ""
    return (
        0 < len(first_line) <= 72
        and not first_line.endswith(".")
        and first_line[0].isascii()
        and first_line[0].isalpha()
    )
