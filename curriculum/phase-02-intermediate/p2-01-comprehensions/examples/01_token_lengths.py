# Measure prompts with comprehensions: lengths, a dict, and a filter.
prompts = [
    "Summarize this report",
    "Hi",
    "Translate the text to French",
    "What is RAG?",
]

lengths = [len(p.split()) for p in prompts]
print(lengths)

by_prompt = {p: len(p.split()) for p in prompts}
print(by_prompt["Hi"])

long_prompts = [p for p in prompts if len(p.split()) >= 3]
print(long_prompts)

longest = max(lengths)
print("longest prompt has", longest, "words")
