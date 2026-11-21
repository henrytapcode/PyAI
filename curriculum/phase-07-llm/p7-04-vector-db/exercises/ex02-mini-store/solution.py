import numpy as np


def _matches_where(meta: dict, where: dict | None) -> bool:
    if not where:
        return True
    for key, val in where.items():
        if key not in meta:
            return False
        if isinstance(val, list):
            if meta[key] not in val:
                return False
        elif meta[key] != val:
            return False
    return True


class MiniStore:
    """Minimal in-memory vector store supporting batch upsert add, pre-filter search, and delete."""

    def __init__(self, client) -> None:
        self._client = client
        self._matrix: np.ndarray | None = None
        self._id_to_idx: dict[str, int] = {}
        self._ids: list[str] = []
        self._texts: list[str] = []
        self._metadatas: list[dict] = []

    def __len__(self) -> int:
        return len(self._id_to_idx)

    def add(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        if len(ids) != len(texts) or (metadatas is not None and len(metadatas) != len(ids)):
            raise ValueError("ids, texts, and metadatas must have the same length")
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate id in batch")
        if not ids:
            return
        metas = [{} for _ in ids] if metadatas is None else [dict(m) for m in metadatas]
        vecs = np.array(self._client.embed(texts), dtype=float)
        new_indices: list[int] = []
        for i, cid in enumerate(ids):
            if cid in self._id_to_idx:
                idx = self._id_to_idx[cid]
                self._texts[idx] = texts[i]
                self._metadatas[idx] = metas[i]
                assert self._matrix is not None
                self._matrix[idx] = vecs[i]
            else:
                new_indices.append(i)
        if new_indices:
            new_vecs = vecs[new_indices]
            self._matrix = new_vecs if self._matrix is None else np.vstack([self._matrix, new_vecs])
            for i in new_indices:
                self._id_to_idx[ids[i]] = len(self._ids)
                self._ids.append(ids[i])
                self._texts.append(texts[i])
                self._metadatas.append(metas[i])

    def search(
        self,
        query: str,
        k: int = 3,
        where: dict | None = None,
    ) -> list[tuple[str, float]]:
        if self._matrix is None or k <= 0:
            return []
        kept = [i for i, meta in enumerate(self._metadatas) if _matches_where(meta, where)]
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
        if doc_id not in self._id_to_idx:
            raise KeyError(doc_id)
        idx = self._id_to_idx.pop(doc_id)
        self._ids.pop(idx)
        self._texts.pop(idx)
        self._metadatas.pop(idx)
        for cid, pos in list(self._id_to_idx.items()):
            if pos > idx:
                self._id_to_idx[cid] = pos - 1
        self._matrix = None if not self._ids else np.delete(self._matrix, idx, axis=0)
