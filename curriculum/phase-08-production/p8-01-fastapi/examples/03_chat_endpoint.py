# Chat endpoint backed by FakeLLM returning answer text and token usage.

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pyai_llm import FakeLLM
from pydantic import BaseModel, Field

app = FastAPI()
llm = FakeLLM(seed=0)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    temperature: float = Field(default=0.0, ge=0.0, le=1.0)


@app.post("/chat")
def chat(body: ChatRequest) -> dict[str, object]:
    reply = llm.chat(
        [{"role": "user", "content": body.message}],
        temperature=body.temperature,
    )
    return {"answer": reply.content, "tokens": reply.usage.total_tokens}


client = TestClient(app)
prompts = [
    "What is RAG?",
    "What is a token?",
    "What is temperature?",
]

total_tokens = 0
for msg in prompts:
    r = client.post("/chat", json={"message": msg})
    data = r.json()
    total_tokens += data["tokens"]
    print(f"{r.status_code} tokens={data['tokens']} answer={data['answer'][:45]}...")

print("total_tokens:", total_tokens)

bad = client.post("/chat", json={"message": "Hi", "temperature": 2})
errs = [(e["loc"], e["type"]) for e in bad.json()["detail"]]
print("bad temp:", bad.status_code, errs)
