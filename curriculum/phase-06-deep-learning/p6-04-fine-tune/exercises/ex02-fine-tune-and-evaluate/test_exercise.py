import torch

from exercise import accuracy, fine_tune, load_model, predict

TRAIN_TEXTS = [
    "Login page crashes with 500 error",
    "Export button freezes on click",
    "Search API returns blank data",
    "Mobile app throws a timeout",
    "Dashboard loops forever",
    "File upload drops the session",
    "Settings page crashes on save",
    "Report page fails with 500 error",
    "App freezes during CSV export",
    "Timeout when opening workspace",
    "Credit card was charged twice",
    "Monthly invoice shows wrong total",
    "Annual plan failed to refund",
    "Team seat billed after cancel",
    "Pro renewal pending too long",
    "Tax receipt shows wrong amount",
    "Overcharged for inactive seats",
    "Discount code missing from invoice",
    "Corporate card billed twice",
    "Refund missing on monthly bill",
]
TRAIN_LABELS = [0] * 10 + [1] * 10

EVAL_TEXTS = [
    "Profile page crashes with 500",
    "Checkout button freezes on click",
    "Search tool throws a timeout",
    "Upload widget loops forever",
    "Credit card billed after cancel",
    "Invoice shows duplicate charge",
    "Annual renewal charged twice",
    "Need refund for wrong total",
]
EVAL_LABELS = [0] * 4 + [1] * 4


def test_fine_tune_returns_python_float_list_of_length_epochs():
    model = load_model()
    losses = fine_tune(model, TRAIN_TEXTS, TRAIN_LABELS, lr=5e-4, epochs=4)
    assert losses is not None, "fine_tune returned None: did you forget to return losses?"
    assert len(losses) == 4
    assert all(type(loss) is float for loss in losses), "each loss must be a Python float"


def test_fine_tune_decreases_loss():
    model = load_model()
    losses = fine_tune(model, TRAIN_TEXTS, TRAIN_LABELS, lr=5e-4, epochs=6)
    assert losses is not None, "fine_tune returned None: did you forget to return losses?"
    assert losses[-1] < losses[0], "training loss should decrease over epochs"


def test_fine_tune_raises_eval_accuracy_above_threshold():
    model = load_model()
    losses = fine_tune(model, TRAIN_TEXTS, TRAIN_LABELS, lr=5e-4, epochs=10)
    assert losses is not None, "fine_tune returned None: did you forget to return losses?"
    acc = accuracy(model, EVAL_TEXTS, EVAL_LABELS)
    assert acc is not None, "accuracy returned None: did you forget to return the score?"
    assert acc >= 0.85, f"expected fine-tuned eval accuracy >= 0.85, got {acc}"


def test_accuracy_returns_python_float_in_unit_interval():
    model = load_model()
    acc = accuracy(model, EVAL_TEXTS, EVAL_LABELS)
    assert acc is not None, "accuracy returned None: did you forget to return the score?"
    assert type(acc) is float, "accuracy must return a built-in Python float, not a tensor"
    assert 0.0 <= acc <= 1.0


def test_accuracy_matches_seeded_baseline_and_creates_no_gradients():
    model = load_model()
    acc = accuracy(model, EVAL_TEXTS, EVAL_LABELS)
    assert acc is not None, "accuracy returned None: did you forget to return the score?"
    assert acc == 0.5
    assert all(p.grad is None for p in model.parameters()), (
        "accuracy must run inside torch.no_grad() without creating gradients"
    )


def test_accuracy_is_deterministic_even_after_train_mode():
    model = load_model()
    model.train()
    first = accuracy(model, TRAIN_TEXTS, TRAIN_LABELS)
    assert first is not None, "accuracy returned None: did you forget to return the score?"
    second = accuracy(model, TRAIN_TEXTS, TRAIN_LABELS)
    third = accuracy(model, TRAIN_TEXTS, TRAIN_LABELS)
    assert not model.training, "accuracy must switch the model to model.eval()"
    assert first == second == third, "repeated accuracy calls must match when dropout is off"


def test_predict_returns_string_labels_and_gets_clear_tickets_right():
    model = load_model()
    losses = fine_tune(model, TRAIN_TEXTS, TRAIN_LABELS, lr=5e-4, epochs=10)
    assert losses is not None, "fine_tune returned None: did you forget to return losses?"
    preds = predict(model, ["Login page crashes with 500 error", "Credit card was charged twice"])
    assert preds is not None, "predict returned None: did you forget to return the label list?"
    assert len(preds) == 2
    assert set(preds).issubset({"bug", "billing"})
    assert preds == ["bug", "billing"]


def test_fine_tune_zero_epochs_returns_empty_and_keeps_weights():
    model = load_model()
    before = model.classifier.weight.detach().clone()
    losses = fine_tune(model, TRAIN_TEXTS, TRAIN_LABELS, lr=5e-4, epochs=0)
    assert losses is not None, "fine_tune(..., epochs=0) returned None instead of []"
    assert losses == []
    assert torch.equal(model.classifier.weight, before), "epochs=0 must not modify model weights"
