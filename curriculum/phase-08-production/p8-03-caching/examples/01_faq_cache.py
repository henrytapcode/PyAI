# FAQ response cache with whitespace normalization and FakeLLM hit-rate reporting.

import hashlib
import json

from pyai_llm import FakeLLM


def normalize_question(text: str) -> str:
    return " ".join(text.strip().split())


def make_faq_key(model: str, system: str, question: str) -> str:
    payload = {
        "model": model,
        "system": normalize_question(system),
        "question": normalize_question(question),
        "temperature": 0.0,
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def main() -> None:
    client = FakeLLM()
    model = "fake-mini"
    system = "You are a helpful support assistant."
    cache: dict[str, str] = {}
    hits = 0
    misses = 0

    questions = [
        "What is RAG?",
        "What is a token?",
        "  What is   RAG? ",
        "What is temperature?",
        "What is a token?  ",
        "What is cosine similarity?",
        "What is RAG?",
        "What is hallucination?",
        "  What is  temperature? ",
        "What is tool calling?",
        "What is cosine similarity?",
        "What is a token?",
    ]

    for q in questions:
        key = make_faq_key(model, system, q)
        if key in cache:
            hits += 1
            status = "HIT "
            _reply = cache[key]
        else:
            misses += 1
            status = "MISS"
            resp = client.chat(
                [
                    {"role": "system", "content": system},
                    {"role": "user", "content": normalize_question(q)},
                ],
                temperature=0.0,
            )
            _reply = resp.content or ""
            cache[key] = _reply
        print(f"{status} {q!r}")

    hit_rate = hits / len(questions)
    print(f"total={len(questions)} hits={hits} misses={misses} hit_rate={hit_rate:.2f}")


if __name__ == "__main__":
    main()
