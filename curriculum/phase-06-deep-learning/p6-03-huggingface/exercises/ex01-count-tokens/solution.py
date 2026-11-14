from transformers import AutoTokenizer

REPO = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
REV = "714eb0fa89d2f80546fda750413ed43d93601a13"

tokenizer = AutoTokenizer.from_pretrained(REPO, revision=REV, local_files_only=True)


def count_tokens(texts: list[str]) -> list[int]:
    """Return the number of non-special tokens for each text in texts.

    Example: count_tokens(["Great!", "Chatbot logs!"]) -> [2, 4]
    """
    counts = [len(tokenizer.tokenize(text)) for text in texts]
    return counts
