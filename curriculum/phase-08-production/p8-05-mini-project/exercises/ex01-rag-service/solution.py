from fastapi import FastAPI
from pyai_llm import cosine
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."


class AskRequest(BaseModel):
    """Validated JSON body for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI:
    """Build a fresh FastAPI RAG service with one-time document indexing."""
    app = FastAPI()
    doc_vecs = client.embed([d["text"] for d in docs])

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        q_vec = client.embed([body.question])[0]
        scored = sorted(
            [
                (cosine(q_vec, dv), idx, d)
                for idx, (d, dv) in enumerate(zip(docs, doc_vecs, strict=True))
            ],
            key=lambda item: (-item[0], item[1]),
        )
        hits = [doc for score, _, doc in scored[: body.top_k] if score >= min_score]
        if not hits:
            return {
                "answer": REFUSAL,
                "sources": [],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }

        context_lines = "\n".join(f"[{n}] {doc['text']}" for n, doc in enumerate(hits, 1))
        messages = [
            {
                "role": "system",
                "content": f"Answer using only the provided context.\n\nContext:\n{context_lines}",
            },
            {"role": "user", "content": body.question},
        ]
        resp = client.chat(messages)
        return {
            "answer": resp.content or "",
            "sources": [doc["id"] for doc in hits],
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            },
        }

    return app
