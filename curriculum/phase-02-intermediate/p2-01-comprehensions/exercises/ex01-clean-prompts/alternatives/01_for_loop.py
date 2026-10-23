def clean_prompts(prompts):
    cleaned = []
    for p in prompts:
        text = " ".join(p.split()).lower()
        if text:
            cleaned.append(text)
    return cleaned
