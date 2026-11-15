# Build a compact VectorStore for 8 bilingual FAQ chunks and answer 3 queries.
from dataclasses import dataclass
import numpy as np
from pyai_llm import FakeLLM


@dataclass
class Hit:
    id: str
    score: float
    text: str
    metadata: dict


class VectorStore:
    def __init__(self, client) -> None:
        self._client = client
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._metadatas: list[dict] = []
        self._id_set: set[str] = set()
        self._matrix: np.ndarray | None = None

    def add(self, ids: list[str], texts: list[str], metadatas: list[dict]) -> None:
        if len(set(ids)) != len(ids) or any(cid in self._id_set for cid in ids):
            raise ValueError("duplicate id")
        vecs = np.array(self._client.embed(texts), dtype=float)
        self._matrix = vecs if self._matrix is None else np.vstack([self._matrix, vecs])
        self._ids.extend(ids)
        self._texts.extend(texts)
        self._metadatas.extend(metadatas)
        self._id_set.update(ids)

    def search(self, query: str, k: int = 2, where: dict | None = None) -> list[Hit]:
        if self._matrix is None or k <= 0:
            return []
        kept = [
            i for i, m in enumerate(self._metadatas)
            if not where or all(key in m and m[key] == val for key, val in where.items())
        ]
        if not kept:
            return []
        q = np.array(self._client.embed([query])[0], dtype=float)
        scores = self._matrix[kept] @ q
        order = np.argsort(-scores, kind="stable")[:k]
        return [
            Hit(
                self._ids[kept[int(j)]],
                round(float(scores[int(j)]), 3),
                self._texts[kept[int(j)]],
                self._metadatas[kept[int(j)]],
            )
            for j in order
        ]


CHUNKS = [
    ("faq1", "Full refund within 30 days.", {"topic": "billing", "lang": "en"}),
    ("faq2", "Fast laptop repair in two days.", {"topic": "support", "lang": "en"}),
    ("faq3", "Cheap car rental with insurance.", {"topic": "travel", "lang": "en"}),
    ("faq4", "Report login error to support.", {"topic": "support", "lang": "en"}),
    ("faq5", "Hoan tien refund trong 30 ngay.", {"topic": "billing", "lang": "vi"}),
    ("faq6", "Sua nhanh fast laptop tai cua hang.", {"topic": "support", "lang": "vi"}),
    ("faq7", "Thue xe cheap car theo ngay.", {"topic": "travel", "lang": "vi"}),
    ("faq8", "Bao loi error dang nhap qua email.", {"topic": "support", "lang": "vi"}),
]

store = VectorStore(FakeLLM(embed_dim=256))
store.add([c[0] for c in CHUNKS], [c[1] for c in CHUNKS], [c[2] for c in CHUNKS])

queries = [
    ("money back", None),
    ("affordable vehicle", None),
    ("quick computer repair", {"lang": "vi", "topic": "support"}),
]
for q_text, where in queries:
    print(f"Q: {q_text}" if where is None else f"Q: {q_text} where={where}")
    for hit in store.search(q_text, k=2, where=where):
        print(f"  {hit.id} {hit.score} {hit.text}")
