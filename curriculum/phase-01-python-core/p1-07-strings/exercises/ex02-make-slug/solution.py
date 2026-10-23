def make_slug(title):
    """Return a URL slug: lowercase words joined by single hyphens."""
    title = title.strip()
    title = title.lower()
    words = title.split()
    return "-".join(words)
