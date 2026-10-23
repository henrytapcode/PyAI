def read_clean_lines(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    result = []
    for line in lines:
        if line.strip() != "":
            result.append(line.strip())
    return result
