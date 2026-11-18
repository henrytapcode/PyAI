import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

REFUSAL = "I don't know based on the provided context."


class AskRequest(BaseModel):
    """Validated JSON body for POST /ask."""

    question: str = Field(min_length=1, max_length=300)
    top_k: int = Field(default=2, ge=1, le=5)


class RagService:
    """Encapsulates document matrix indexing, document lookup, and top-k retrieval."""

    def __init__(self, docs: list[dict], client, min_score: float) -> None:
        self.docs = list(docs)
        self.docs_by_id = {d["id"]: {"id": d["id"], "text": d["text"]} for d in self.docs}
        self.client = client
        self.min_score = min_score
        self.vectors = np.array(client.embed([d["text"] for d in self.docs]), dtype=float)

    def _cosine_scores(self, q_vec: np.ndarray) -> np.ndarray:
        if len(self.docs) == 0:
            return np.zeros(0, dtype=float)
        q_norm = float(np.linalg.norm(q_vec))
        doc_norms = np.linalg.norm(self.vectors, axis=1)
        denom = doc_norms * q_norm
        return np.divide(
            self.vectors @ q_vec,
            denom,
            out=np.zeros(len(self.docs), dtype=float),
            where=denom != 0.0,
        )

    def get_document(self, doc_id: str) -> dict[str, str]:
        doc = self.docs_by_id.get(doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="document not found")
        return doc

    def answer(self, question: str, top_k: int) -> dict[str, object]:
        q_vec = np.array(self.client.embed([question])[0], dtype=float)
        scores = self._cosine_scores(q_vec)
        order = np.argsort(-scores, kind="stable")[:top_k]
        matches = [
            (float(scores[int(i)]), self.docs[int(i)])
            for i in order
            if float(scores[int(i)]) >= self.min_score
        ]
        if not matches:
            return {
                "answer": REFUSAL,
                "sources": [],
                "scores": [],
                "usage": {"prompt_tokens": 0, "completion_tokens": 0},
            }

        ctx = "\n".join(f"[{n}] {doc['text']}" for n, (_, doc) in enumerate(matches, 1))
        resp = self.client.chat([
            {"role": "system", "content": f"Answer from context only.\n\nContext:\n{ctx}"},
            {"role": "user", "content": question},
        ])
        reply = resp.content or ""
        if reply == REFUSAL:
            sources: list[str] = []
            hit_scores: list[float] = []
        else:
            sources = [doc["id"] for _, doc in matches]
            hit_scores = [round(score, 3) for score, _ in matches]
        return {
            "answer": reply,
            "sources": sources,
            "scores": hit_scores,
            "usage": {
                "prompt_tokens": resp.usage.prompt_tokens,
                "completion_tokens": resp.usage.completion_tokens,
            },
        }


def create_app(docs: list[dict], client, min_score: float = 0.2) -> FastAPI:
    """Build a FastAPI app backed by a dedicated RagService instance."""
    app = FastAPI()
    service = RagService(docs, client, min_score)

    @app.get("/health")
    def health() -> dict[str, object]:
        return {"status": "ok", "docs": len(service.docs)}

    @app.get("/documents/{doc_id}")
    def get_document(doc_id: str) -> dict[str, str]:
        return service.get_document(doc_id)

    @app.post("/ask")
    def ask(body: AskRequest) -> dict[str, object]:
        return service.answer(body.question, body.top_k)

    return app
