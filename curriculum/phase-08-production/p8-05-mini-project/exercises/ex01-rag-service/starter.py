from fastapi import FastAPI
from pyai_llm import cosine  # noqa: F401
from pydantic import BaseModel, Field  # noqa: F401


def create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI:
    """Create a FastAPI RAG service that indexes ``docs`` once at startup.

    Example:
        app = create_app([{"id": "r1", "text": "Refunds take 5 days."}], client)
        GET /health -> {"status": "ok", "docs": 1}
        POST /ask {"question": "How long do refunds take?"}
            -> {"answer": "Refunds take 5 days. [1]", "sources": ["r1"], "usage": {...}}
    """
    app = FastAPI()
    # TODO: embed [d["text"] for d in docs] once at startup
    # TODO: define AskRequest(question: 1..300, top_k: 1..5 default 2)
    # TODO: register GET /health -> {"status": "ok", "docs": len(docs)}
    # TODO: register POST /ask to retrieve, filter by min_score, refuse or call client.chat
    return app
