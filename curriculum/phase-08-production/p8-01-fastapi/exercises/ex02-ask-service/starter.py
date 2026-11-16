from fastapi import FastAPI, HTTPException  # noqa: F401
from pydantic import BaseModel, Field  # noqa: F401

app = FastAPI()

DOCS: dict[int, str] = {
    1: "FastAPI validates JSON request bodies with Pydantic",
    2: "RAG retrieves relevant document chunks for an LLM",
    3: "TestClient runs FastAPI endpoint tests in Python",
    4: "Pytest fixtures reset state between FastAPI tests",
    5: "Status code 422 means request validation failed",
}


class AskRequest(BaseModel):
    # TODO: add Field constraints (question: 1..200 chars, top_k: 1..5 default 2)
    question: str
    top_k: int = 2


@app.get("/health")
def health() -> dict[str, str] | None:
    """Return service health status.

    Example: GET /health -> {"status": "ok"}
    """
    # TODO: return {"status": "ok"}
    return None


@app.post("/ask")
def ask(body: AskRequest) -> dict[str, object] | None:
    """Rank matching DOCS IDs by lowercase word overlap with body.question.

    Example: AskRequest(question="FastAPI tests", top_k=2)
             -> {"question": "FastAPI tests", "sources": [3, 4]}
    """
    # TODO: split lowercase words, rank by (-overlap, doc_id), slice [:body.top_k],
    #       and raise HTTPException(404, detail="no matching documents") when empty
    return None
