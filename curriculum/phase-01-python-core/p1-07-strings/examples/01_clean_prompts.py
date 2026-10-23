# Normalise messy user prompts: strip, lower-case, collapse spaces, then compare.
def normalize(text):
    words = text.lower().split()
    return " ".join(words)


raw_prompts = [
    "   Summarize THIS   text  ",
    "SUMMARIZE this text",
    "Translate to   French ",
]

seen = []
for raw in raw_prompts:
    clean = normalize(raw)
    if clean in seen:
        print(f"duplicate: {clean}")
    else:
        seen.append(clean)
        print(f"new:       {clean}")

print(f"{len(seen)} unique prompts")
