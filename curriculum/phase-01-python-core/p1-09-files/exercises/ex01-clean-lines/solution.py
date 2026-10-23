def read_clean_lines(path):
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            clean = line.strip()
            if clean:
                lines.append(clean)
    return lines
