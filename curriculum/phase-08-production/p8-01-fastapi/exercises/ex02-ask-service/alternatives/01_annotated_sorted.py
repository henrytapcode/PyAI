from typing import Annotated

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

QuestionText = Annotated[str, Field(min_length=1, max_length=200)]
TopK = Annotated[int, Field(ge=1, le=5)]


class AskRequest(BaseModel):
    question: QuestionText
    top_k: TopK = 2


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


@app.post("/ask")
def ask(body: AskRequest) -> dict[str, object]:
    """Rank matching DOCS IDs using set overlap and sorted()."""
    q_words = set(body.question.lower().split())
    matches = [
        (len(q_words & set(text.lower().split())), doc_id)
        for doc_id, text in DOCS.items()
    ]
    ranked = sorted(
        (pair for pair in matches if pair[0] > 0),
        key=lambda pair: (-pair[0], pair[1]),
    )
    if not ranked:
        raise HTTPException(status_code=404, detail="no matching documents")
    return {
        "question": body.question,
        "sources": [doc_id for _, doc_id in ranked[: body.top_k]],
    }
