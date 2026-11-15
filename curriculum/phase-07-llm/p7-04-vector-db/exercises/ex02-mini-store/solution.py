import numpy as np


class MiniStore:
    """Minimal in-memory vector store supporting batch add, pre-filter search, and delete."""

    def __init__(self, client) -> None:
        self._client = client
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._metadatas: list[dict] = []
        self._id_set: set[str] = set()
        self._matrix: np.ndarray | None = None

    def __len__(self) -> int:
        return len(self._ids)

    def add(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        if len(ids) != len(texts) or (metadatas is not None and len(metadatas) != len(ids)):
            raise ValueError("ids, texts, and metadatas must have the same length")
        if len(set(ids)) != len(ids) or any(cid in self._id_set for cid in ids):
            raise ValueError("duplicate id")
        if not ids:
            return
        metas = [{} for _ in ids] if metadatas is None else [dict(m) for m in metadatas]
        vecs = np.array(self._client.embed(texts), dtype=float)
        self._matrix = vecs if self._matrix is None else np.vstack([self._matrix, vecs])
        self._ids.extend(ids)
        self._texts.extend(texts)
        self._metadatas.extend(metas)
        self._id_set.update(ids)

    def search(
        self,
        query: str,
        k: int = 3,
        where: dict | None = None,
    ) -> list[tuple[str, float]]:
        if self._matrix is None or k <= 0:
            return []
        kept = [
            i
            for i, meta in enumerate(self._metadatas)
            if not where or all(key in meta and meta[key] == val for key, val in where.items())
        ]
        if not kept:
            return []
        q = np.array(self._client.embed([query])[0], dtype=float)
        scores = self._matrix[kept] @ q
        order = np.argsort(-scores, kind="stable")[:k]
        return [
            (self._ids[kept[int(j)]], round(float(scores[int(j)]), 3))
            for j in order
        ]

    def delete(self, doc_id: str) -> None:
        if doc_id not in self._id_set:
            raise KeyError(doc_id)
        idx = self._ids.index(doc_id)
        self._ids.pop(idx)
        self._texts.pop(idx)
        self._metadatas.pop(idx)
        self._id_set.remove(doc_id)
        self._matrix = None if not self._ids else np.delete(self._matrix, idx, axis=0)
