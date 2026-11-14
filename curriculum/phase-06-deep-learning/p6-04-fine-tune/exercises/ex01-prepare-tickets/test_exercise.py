from exercise import class_counts, encode, split_data

SAMPLE_TEXTS = [f"ticket {i}" for i in range(20)]
SAMPLE_LABELS = [i % 2 for i in range(20)]


def test_split_data_returns_expected_split_sizes():
    res = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=27)
    assert res is not None, "split_data returned None: did you forget to return the 6-tuple?"
    train_x, train_y, val_x, val_y, test_x, test_y = res
    assert (len(train_x), len(val_x), len(test_x)) == (12, 4, 4)
    assert (len(train_y), len(val_y), len(test_y)) == (12, 4, 4)


def test_split_data_keeps_text_and_label_pairs_aligned():
    res = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=27)
    assert res is not None, "split_data returned None: did you forget to return the 6-tuple?"
    train_x, train_y, val_x, val_y, test_x, test_y = res
    expected = dict(zip(SAMPLE_TEXTS, SAMPLE_LABELS, strict=True))
    for xs, ys in ((train_x, train_y), (val_x, val_y), (test_x, test_y)):
        for text, label in zip(xs, ys, strict=True):
            assert expected[text] == label, "text and label must stay paired after shuffling"


def test_split_data_produces_disjoint_splits_covering_all_items():
    res = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=27)
    assert res is not None, "split_data returned None: did you forget to return the 6-tuple?"
    train_x, _, val_x, _, test_x, _ = res
    assert set(train_x).isdisjoint(val_x)
    assert set(train_x).isdisjoint(test_x)
    assert set(val_x).isdisjoint(test_x)
    assert set(train_x) | set(val_x) | set(test_x) == set(SAMPLE_TEXTS)


def test_split_data_is_deterministic_with_same_seed():
    first = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=27)
    second = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=27)
    other = split_data(SAMPLE_TEXTS, SAMPLE_LABELS, val_frac=0.2, test_frac=0.2, seed=99)
    assert first is not None, "split_data returned None: did you forget to return the 6-tuple?"
    assert first == second, "same seed must produce the exact same split"
    assert first[0] != other[0], "different seeds should shuffle items differently"


def test_encode_returns_tensors_with_expected_keys_and_shape():
    batch = encode(["App crashes", "Credit card charged twice today"], max_length=16)
    assert batch is not None, "encode returned None: did you forget to return the batch dict?"
    assert "input_ids" in batch and "attention_mask" in batch
    ids = batch["input_ids"]
    mask = batch["attention_mask"]
    assert ids.shape == mask.shape
    assert ids.shape[0] == 2
    assert ids.shape[1] <= 16


def test_encode_truncates_long_text_to_max_length():
    long_text = " ".join(["error"] * 30)
    batch = encode([long_text, "ok"], max_length=8)
    assert batch is not None, "encode returned None: did you forget to return the batch dict?"
    assert tuple(batch["input_ids"].shape) == (2, 8)
    assert tuple(batch["attention_mask"].shape) == (2, 8)


def test_encode_attention_mask_marks_real_tokens_and_padding():
    batch = encode(["Hi", "Login page crashes with 500 error"], max_length=16)
    assert batch is not None, "encode returned None: did you forget to return the batch dict?"
    mask = batch["attention_mask"]
    assert set(mask.flatten().tolist()).issubset({0, 1})
    assert mask[0].tolist()[-1] == 0, "shorter sentence should be padded with 0 in attention_mask"
    assert mask[1].tolist().count(1) > mask[0].tolist().count(1)


def test_class_counts_counts_each_label():
    counts = class_counts([0, 1, 0, 0, 1])
    assert counts is not None, "class_counts returned None: did you forget to return the dict?"
    assert counts == {0: 3, 1: 2}


def test_class_counts_empty_list_returns_empty_dict():
    counts = class_counts([])
    assert counts is not None, "class_counts returned None instead of {}"
    assert counts == {}
