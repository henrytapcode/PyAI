# Measuring accuracy before and after fine-tuning

**What it shows:** Benchmarking BERT-Tiny's randomly initialised classification head on the test split (`0.562`), fine-tuning for 10 full-batch epochs with `AdamW`, and measuring the jump (`0.938`).

**Step by step**
1. Lines 28–34 define `accuracy()`, switching to `model.eval()` and `torch.no_grad()` so dropout is off and no gradients are tracked.
2. Lines 43–51 load the pinned tokenizer and base model (`torch.manual_seed(0)` right before loading) with `num_labels=2` and custom `id2label`/`label2id`.
3. Line 53 records `before` (`0.562`), lines 58–63 run 10 full-batch steps using `out = model(**train_batch, labels=train_y_t)` and `AdamW(lr=5e-4)`, and lines 65–68 print `before`, `after`, and `gain`.

**Notice:** Calling `torch.manual_seed(0)` immediately before `from_pretrained()` makes both the random classification head weights and the training dropout reproducible.

**Try it yourself:** Set `lr=1e-1` instead of `5e-4` and observe how the accuracy after training fails to climb cleanly.
