# A tiny keyword search: Document and Hit dataclasses, results sorted best first.
from dataclasses import dataclass, field


@dataclass
class Document:
    doc_id: str
    text: str
    tags: list = field(default_factory=list)


@dataclass(order=True)
class Hit:
    score: int
    doc_id: str


docs = [
    Document("d1", "python lists and dicts", tags=["python"]),
    Document("d2", "python dataclasses make records easy"),
    Document("d3", "cooking pasta at home"),
    Document("d4", "python python python"),
]


def search(documents, word):
    hits = []
    for doc in documents:
        score = doc.text.split().count(word)
        if score > 0:
            hits.append(Hit(score, doc.doc_id))
    return sorted(hits, reverse=True)


results = search(docs, "python")
for hit in results:
    print(hit)
print("best:", results[0].doc_id)
print("tags of d1:", docs[0].tags)
print("tags of d2:", docs[1].tags)
