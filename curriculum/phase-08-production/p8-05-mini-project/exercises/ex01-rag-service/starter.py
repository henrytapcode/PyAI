from fastapi import FastAPI, HTTPException  # noqa: F401
from pyai_llm import cosine  # noqa: F401
from pydantic import BaseModel, Field  # noqa: F401

REFUSAL = "I don't know based on the provided context."


def create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI:
    """Create a FastAPI RAG service that indexes ``docs`` once at startup.

    Example:
        app = create_app([{"id": "r1", "text": "Refunds take 5 days."}], client)
        GET /health -> {"status": "ok", "docs": 1}
        GET /documents/r1 -> {"id": "r1", "text": "Refunds take 5 days."}
        POST /ask {"question": "How long do refunds take?"}
            -> {"answer": "...", "sources": ["r1"], "scores": [0.712], "usage": {...}}
    """
    app = FastAPI()
    # TODO: embed [d["text"] for d in docs] once at startup and index docs by id
    # TODO: define AskRequest(question: 1..300, top_k: 1..5 default 2)
    # TODO: register GET /health -> {"status": "ok", "docs": len(docs)}
    # TODO: register GET /documents/{doc_id} -> doc dict or 404 {"detail": "document not found"}
    # TODO: register POST /ask with scores, min_score refusal, and model-refusal source clearing
    return app
