# Save a VectorStore to JSON, reload without re-embedding, delete an id, and re-search.
import json
import numpy as np
from pyai_llm import FakeLLM


class CountingClient:
    def __init__(self, inner) -> None:
        self._inner = inner
        self.embed_calls = 0

    def embed(self, texts: list[str]) -> list[list[float]]:
        self.embed_calls += 1
        return self._inner.embed(texts)


class VectorStore:
    def __init__(self, client) -> None:
        self._client = client
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._metadatas: list[dict] = []
        self._matrix: np.ndarray | None = None

    def __len__(self) -> int:
        return len(self._ids)

    def add(self, ids: list[str], texts: list[str], metadatas: list[dict]) -> None:
        vecs = np.array(self._client.embed(texts), dtype=float)
        self._matrix = vecs if self._matrix is None else np.vstack([self._matrix, vecs])
        self._ids.extend(ids)
        self._texts.extend(texts)
        self._metadatas.extend(metadatas)

    def delete(self, doc_id: str) -> None:
        if doc_id not in self._ids:
            raise KeyError(doc_id)
        idx = self._ids.index(doc_id)
        self._ids.pop(idx)
        self._texts.pop(idx)
        self._metadatas.pop(idx)
        self._matrix = None if not self._ids else np.delete(self._matrix, idx, axis=0)

    def search(self, query: str, k: int = 2) -> list[tuple[str, float]]:
        if self._matrix is None or k <= 0:
            return []
        q = np.array(self._client.embed([query])[0], dtype=float)
        scores = self._matrix @ q
        order = np.argsort(-scores, kind="stable")[:k]
        return [(self._ids[int(i)], round(float(scores[int(i)]), 3)) for i in order]

    def to_json(self) -> str:
        return json.dumps({
            "ids": self._ids,
            "texts": self._texts,
            "metadatas": self._metadatas,
            "vectors": [] if self._matrix is None else self._matrix.tolist(),
        })

    @classmethod
    def from_json(cls, raw: str, client) -> "VectorStore":
        data = json.loads(raw)
        store = cls(client)
        store._ids = list(data["ids"])
        store._texts = list(data["texts"])
        store._metadatas = [dict(m) for m in data["metadatas"]]
        vecs = data["vectors"]
        store._matrix = np.array(vecs, dtype=float) if vecs else None
        return store


client = CountingClient(FakeLLM(embed_dim=256))
store = VectorStore(client)
store.add(
    ["c1", "c2", "c3"],
    ["Full refund for broken laptop.", "Fast money back for notebook.", "Cheap car rental."],
    [{"topic": "billing"}, {"topic": "billing"}, {"topic": "travel"}],
)
print("before save -> len:", len(store), "embed_calls:", client.embed_calls)
print("before search:", store.search("money back for laptop", k=2))

snapshot = store.to_json()
reload_client = CountingClient(FakeLLM(embed_dim=256))
reloaded = VectorStore.from_json(snapshot, reload_client)
print("after reload -> len:", len(reloaded), "embed_calls:", reload_client.embed_calls)
print("reloaded search:", reloaded.search("money back for laptop", k=2))

reloaded.delete("c2")
print("after delete c2 -> len:", len(reloaded))
print("after delete search:", reloaded.search("money back for laptop", k=2))
