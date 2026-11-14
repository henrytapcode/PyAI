# Saving, reloading, and predicting new tickets

**What it shows:** Fine-tuning BERT-Tiny, saving both model and tokenizer to a temporary folder with `save_pretrained()`, reloading them offline, and classifying four brand-new tickets.

**Step by step**
1. Lines 33–53 load the pinned model (`id2label={0: "bug", 1: "billing"}`) and run 10 fine-tuning steps with `AdamW(lr=5e-4)` on the 48 training tickets.
2. Lines 62–66 open a `tempfile.TemporaryDirectory()`, write the fine-tuned weights, config, and tokenizer files with `save_pretrained(tmp)`, and reload both from `tmp`.
3. Lines 67–69 build a `pipeline("text-classification", ...)` from the reloaded objects and print each predicted text label beside its ticket.

**Notice:** Always save the tokenizer alongside the model in the same folder so the reloaded model receives the exact same vocabulary IDs and special tokens.

**Try it yourself:** Add a tricky mixed ticket such as `"App crashed while downloading my invoice"` to `new_tickets` and see which label it predicts.
