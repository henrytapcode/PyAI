from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

DOCS: dict[int, str] = {
    1: "FastAPI validates JSON request bodies with Pydantic",
    2: "RAG retrieves relevant document chunks for an LLM",
    3: "TestClient runs FastAPI endpoint tests in Python",
    4: "Pytest fixtures reset state between FastAPI tests",
    5: "Status code 422 means request validation failed",
}


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=200)
    top_k: int = Field(default=2, ge=1, le=5)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


@app.post("/ask")
def ask(body: AskRequest) -> dict[str, object]:
    """Rank matching DOCS IDs by lowercase word overlap with body.question."""
    q_words = set(body.question.lower().split())
    scored: list[tuple[int, int]] = []
    for doc_id, text in DOCS.items():
        overlap = len(q_words & set(text.lower().split()))
        if overlap > 0:
            scored.append((overlap, doc_id))

    if not scored:
        raise HTTPException(status_code=404, detail="no matching documents")

    scored.sort(key=lambda item: (-item[0], item[1]))
    sources = [doc_id for _, doc_id in scored[: body.top_k]]
    return {"question": body.question, "sources": sources}
