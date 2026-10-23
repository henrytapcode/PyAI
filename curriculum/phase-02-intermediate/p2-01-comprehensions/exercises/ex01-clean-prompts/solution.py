def clean_prompts(prompts):
    """Return the prompts lowercased, with extra spaces removed and empty ones dropped.

    Example: clean_prompts(["  Hi   THERE ", "   "]) returns ["hi there"]
    """
    return [" ".join(p.split()).lower() for p in prompts if p.strip()]
