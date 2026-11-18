from fastapi import FastAPI, HTTPException
from pyai_llm import cosine
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."


class AskRequest(BaseModel):
    """Validated JSON payload for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


def _select_matches(
    docs: list[dict],
    doc_vecs: list[list[float]],
    query_vec: list[float],
    top_k: int,
    min_score: float,
) -> list[tuple[float, dict]]:
    """Rank documents by cosine similarity and keep top_k hits >= min_score."""
    ranked: list[tuple[float, int, dict]] = []
    for idx, doc in enumerate(docs):
        similarity = cosine(query_vec, doc_vecs[idx])
        ranked.append((similarity, idx, doc))
    ranked.sort(key=lambda entry: (-entry[0], entry[1]))
    return [(score, doc) for score, _, doc in ranked[:top_k] if score >= min_score]


def _build_prompt(matches: list[tuple[float, dict]], question: str) -> list[dict]:
    """Format numbered context chunks and user question for client.chat."""
    numbered = "\n".join(
        f"[{pos}] {doc['text']}" for pos, (_, doc) in enumerate(matches, start=1)
    )
    system_msg = f"Answer using only the provided context.\n\nContext:\n{numbered}"
    return [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": question},
    ]


def create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI:
    """Build a fresh FastAPI RAG service with document lookup and score reporting."""
    app = FastAPI()
    docs_by_id = {doc["id"]: {"id": doc["id"], "text": doc["text"]} for doc in docs}
    doc_vecs = client.embed([doc["text"] for doc in docs])

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(docs)}

    @app.get("/documents/{doc_id}")
    def get_document(doc_id: str) -> dict[str, str]:
        doc = docs_by_id.get(doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="document not found")
        return doc

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        query_vec = client.embed([body.question])[0]
        matches = _select_matches(docs, doc_vecs, query_vec, body.top_k, min_score)
        if not matches:
            return {
                "answer": REFUSAL,
                "sources": [],
                "scores": [],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }

        resp = client.chat(_build_prompt(matches, body.question))
        answer = resp.content or ""
        if answer == REFUSAL:
            sources: list[str] = []
            scores: list[float] = []
        else:
            sources = [doc["id"] for _, doc in matches]
            scores = [round(score, 3) for score, _ in matches]
        return {
            "answer": answer,
            "sources": sources,
            "scores": scores,
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            },
        }

    return app
