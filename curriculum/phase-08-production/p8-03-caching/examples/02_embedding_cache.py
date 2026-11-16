# Embedding cache that batches only modified or unseen documents and preserves order.

from pyai_llm import FakeLLM


def embed_batch_cached(
    client: FakeLLM,
    model: str,
    texts: list[str],
    cache: dict[tuple[str, str], list[float]],
) -> tuple[list[list[float]], int]:
    missing: list[str] = []
    seen_missing: set[str] = set()
    for text in texts:
        key = (model, text)
        if key not in cache and text not in seen_missing:
            missing.append(text)
            seen_missing.add(text)

    if missing:
        vectors = client.embed(missing)
        for text, vec in zip(missing, vectors, strict=True):
            cache[(model, text)] = vec

    ordered = [cache[(model, text)] for text in texts]
    return ordered, len(missing)


def main() -> None:
    client = FakeLLM(embed_dim=16)
    model = "embed-v1"
    cache: dict[tuple[str, str], list[float]] = {}

    docs_v1 = [
        "Reset your password in account settings.",
        "Invoices are emailed on the first of each month.",
        "Refunds return to your original payment method.",
        "Two-factor authentication protects your login.",
        "Support replies within one business day.",
        "API keys must be kept out of Docker images.",
    ]

    vecs_v1, sent_1 = embed_batch_cached(client, model, docs_v1, cache)
    print(f"Run 1: sent {sent_1}/{len(docs_v1)} texts to embed()")

    docs_v2 = list(docs_v1)
    docs_v2[1] = "Invoices are emailed and downloadable as PDF."
    docs_v2[4] = "Support replies within four business hours."

    vecs_v2, sent_2 = embed_batch_cached(client, model, docs_v2, cache)
    print(f"Run 2: sent {sent_2}/{len(docs_v2)} texts to embed()")

    fresh = client.embed(docs_v2)
    print("match:", vecs_v2 == fresh)
    print("unchanged doc 0 reused:", vecs_v2[0] == vecs_v1[0])


if __name__ == "__main__":
    main()
