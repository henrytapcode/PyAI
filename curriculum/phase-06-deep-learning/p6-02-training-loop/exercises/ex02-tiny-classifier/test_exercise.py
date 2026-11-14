import torch
import torch.nn as nn

from exercise import TinyClassifier, accuracy


def test_output_shape_matches_batch_and_classes():
    torch.manual_seed(0)
    model = TinyClassifier(in_features=2, hidden=8, classes=3)
    logits = model(torch.randn(5, 2))
    assert logits is not None, (
        "TinyClassifier.forward returned None: did you forget to return logits?"
    )
    assert tuple(logits.shape) == (5, 3)


def test_parameter_count_matches_architecture():
    torch.manual_seed(0)
    model = TinyClassifier(in_features=2, hidden=8, classes=3)
    total = sum(p.numel() for p in model.parameters())
    assert total == 51, "expected 2*8 + 8 + 8*3 + 3 = 51 parameters"


def test_accuracy_matches_hand_set_weights():
    model = nn.Linear(2, 2)
    with torch.no_grad():
        model.weight.copy_(torch.tensor([[1.0, 0.0], [-1.0, 0.0]]))
        model.bias.zero_()
    xs = torch.tensor([[2.0, 0.0], [1.0, 5.0], [-3.0, 0.0], [-1.0, 2.0]])
    # Predicted classes from weights: [0, 0, 1, 1]; 3 out of 4 match ys
    ys = torch.tensor([0, 1, 1, 1])
    acc = accuracy(model, xs, ys)
    assert acc is not None, "accuracy returned None: did you forget to return the value?"
    assert acc == 0.75


def test_accuracy_returns_python_float_in_unit_interval():
    torch.manual_seed(0)
    model = nn.Linear(2, 2)
    xs = torch.randn(10, 2)
    ys = torch.zeros(10, dtype=torch.int64)
    acc = accuracy(model, xs, ys)
    assert acc is not None, "accuracy returned None: did you forget to return the value?"
    assert type(acc) is float, "accuracy must return a built-in Python float, not a tensor"
    assert 0.0 <= acc <= 1.0


def test_accuracy_sets_eval_mode_and_creates_no_gradients():
    torch.manual_seed(0)
    model = nn.Linear(2, 2)
    model.train()
    xs = torch.randn(6, 2)
    ys = torch.zeros(6, dtype=torch.int64)
    acc = accuracy(model, xs, ys)
    assert acc is not None, "accuracy returned None: did you forget to return the value?"
    assert not model.training, "accuracy must call model.eval()"
    assert all(p.grad is None for p in model.parameters()), (
        "accuracy must not populate parameter gradients"
    )


def test_short_training_on_two_blobs_reaches_high_accuracy():
    torch.manual_seed(0)
    c0 = torch.randn(60, 2) * 0.5 + torch.tensor([-1.0, -1.0])
    c1 = torch.randn(60, 2) * 0.5 + torch.tensor([1.0, 1.0])
    xs = torch.cat([c0, c1], dim=0)
    ys = torch.cat([torch.zeros(60, dtype=torch.int64), torch.ones(60, dtype=torch.int64)])

    model = TinyClassifier(in_features=2, hidden=8, classes=2)
    assert sum(p.numel() for p in model.parameters()) > 0, "TinyClassifier has no layers yet"
    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.2)
    for _ in range(30):
        logits = model(xs)
        assert logits is not None, "TinyClassifier.forward returned None"
        loss = loss_fn(logits, ys)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    acc = accuracy(model, xs, ys)
    assert acc is not None, "accuracy returned None"
    assert acc >= 0.9
