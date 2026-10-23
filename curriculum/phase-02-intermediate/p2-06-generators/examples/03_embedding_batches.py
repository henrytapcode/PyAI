# Clean documents, then send them to a fake embedding model in batches with a character budget.
def batches_by_budget(texts, max_chars):
    batch = []
    used = 0
    for text in texts:
        if batch and used + len(text) > max_chars:
            yield batch
            batch = []
            used = 0
        batch.append(text)
        used += len(text)
    if batch:
        yield batch


def fake_embed(batch):
    return [len(text) for text in batch]


documents = [
    "  Intro to RAG ",
    "",
    "Vector databases",
    "   ",
    "Chunking text",
    "Prompt design",
    "Evals",
    "Agents and tools",
    "Memory",
]

cleaned = (d.strip() for d in documents)
non_empty = (d for d in cleaned if d)

call_number = 0
for batch in batches_by_budget(non_empty, 30):
    call_number += 1
    sizes = fake_embed(batch)
    print("call", call_number, "->", len(batch), "texts", sizes, "total", sum(sizes))
