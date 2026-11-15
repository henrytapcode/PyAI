from dataclasses import dataclass


@dataclass
class _Record:
    id: str
    text: str
    metadata: dict
    vector: list[float]


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
    """Alternative MiniStore keeping dataclass records in a list and scoring in a loop."""

    def __init__(self, client) -> None:
        self._client = client
        self._records: list[_Record] = []
        self._id_to_index: dict[str, int] = {}

    def __len__(self) -> int:
        return len(self._records)

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
        vectors = self._client.embed(texts)
        for cid, text, meta, vec in zip(ids, texts, metas, vectors, strict=True):
            record = _Record(cid, text, meta, list(vec))
            if cid in self._id_to_index:
                self._records[self._id_to_index[cid]] = record
            else:
                self._id_to_index[cid] = len(self._records)
                self._records.append(record)

    def search(
        self,
        query: str,
        k: int = 3,
        where: dict | None = None,
    ) -> list[tuple[str, float]]:
        if not self._records or k <= 0:
            return []
        eligible = [rec for rec in self._records if _matches_where(rec.metadata, where)]
        if not eligible:
            return []
        q = self._client.embed([query])[0]
        scored: list[tuple[str, float]] = []
        for rec in eligible:
            dot = sum(a * b for a, b in zip(rec.vector, q, strict=True))
            scored.append((rec.id, float(dot)))
        scored.sort(key=lambda item: -item[1])
        return [(cid, round(score, 3)) for cid, score in scored[:k]]

    def delete(self, doc_id: str) -> None:
        if doc_id not in self._id_to_index:
            raise KeyError(doc_id)
        idx = self._id_to_index.pop(doc_id)
        self._records.pop(idx)
        for rec_id, rec_idx in list(self._id_to_index.items()):
            if rec_idx > idx:
                self._id_to_index[rec_id] = rec_idx - 1
