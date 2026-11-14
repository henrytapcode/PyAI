# Computing softmax and labels by hand vs. `pipeline()`

**What it shows:** Running the tokenizer and model manually with `model.eval()` and `torch.no_grad()`, applying `softmax` and `argmax`, and confirming the results match `pipeline()`.

**Step by step**
1. Lines 5–11 load `tokenizer` and `model` once from cache and put the model in `eval()` mode.
2. Lines 19–21 tokenize three sentences into PyTorch tensors and run `model(**batch)` inside `with torch.no_grad():` to get raw `logits`.
3. Lines 23–30 compute `torch.softmax(logits, dim=1)`, pick the winning index per row with `argmax(dim=1)`, and map each index using `model.config.id2label`.
4. Lines 32–34 build `pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)` from the exact same objects and verify `manual == from_pipe` prints `match: True`.

**Notice:** Calling `model.eval()` and `with torch.no_grad():` skips gradient tracking during manual inference, and `torch.softmax(..., dim=1)` matches the exact scores returned by `pipeline()`.

**Try it yourself:** Print `logits.tolist()` before `softmax` to see the raw unnormalised scores that produced each `0.991` or `0.999` probability.
