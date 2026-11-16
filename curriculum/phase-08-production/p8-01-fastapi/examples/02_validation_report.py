# Validation report comparing valid and invalid AskRequest payloads.

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=200)
    top_k: int = Field(default=3, ge=1, le=5)


@app.post("/ask")
def ask(body: AskRequest) -> dict[str, object]:
    return {"question": body.question, "top_k": body.top_k}


client = TestClient(app)
cases = [
    {"question": "What is RAG?", "top_k": 2},
    {"top_k": 2},
    {"question": ""},
    {"question": "What is RAG?", "top_k": 9},
    {"question": "What is RAG?", "top_k": "many"},
]

print(f"{'#':>2s}  {'status':>6s}  {'detail'}")
for idx, payload in enumerate(cases, 1):
    r = client.post("/ask", json=payload)
    if r.status_code == 200:
        detail = "ok"
    else:
        first = r.json()["detail"][0]
        detail = f"{first['loc']} -> {first['type']}"
    print(f"{idx:>2d}  {r.status_code:>6d}  {detail}")
