def normalize(text):
    return " ".join(text.lower().split())


def clean_prompts(prompts):
    normalized = [normalize(p) for p in prompts]
    return [text for text in normalized if text]
