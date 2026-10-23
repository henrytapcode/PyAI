def make_slug(title):
    parts = []
    for word in title.split():
        parts.append(word.lower())
    return "-".join(parts)
