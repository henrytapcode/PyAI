def make_slug(title):
    """Return a URL slug: lowercase words joined by single hyphens.

    Example: make_slug("  Python   For AI  ") returns "python-for-ai"
    """
    # This code runs, but it has bugs. Find them and fix them.
    title.strip()
    title.lower()
    words = title.split(" ")
    return "_".join(words)
