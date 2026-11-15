import numpy as np


class MiniStore:
    """Minimal in-memory vector store supporting batch upsert add, pre-filter search, and delete."""

    def __init__(self, client) -> None:
        # TODO: initialize storage for ids, texts, metadatas, and vectors
        pass

    def __len__(self) -> int:
        # TODO: return number of stored records
        return None

    def add(
        self,
        ids: list[str],
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> None:
        # TODO: validate unique ids, batch-embed texts once, and append records
        pass

    def search(
        self,
        query: str,
        k: int = 3,
        where: dict | None = None,
    ) -> list[tuple[str, float]]:
        # TODO: pre-filter by where, score matching rows, return top-k (id, score)
        return None

    def delete(self, doc_id: str) -> None:
        # TODO: remove record and vector by id, or raise KeyError if missing
        pass
