from transformers import pipeline

from exercise import classify, model, negatives, tokenizer


def test_classify_returns_correct_labels_for_clear_sentences():
    texts = [
        "Fast and helpful answer, solved my bug!",
        "The bot kept repeating the wrong link.",
        "Nice summary, very easy to follow.",
    ]
    result = classify(texts)
    assert result is not None, "classify returned None: did you forget to return the list?"
    labels = [label for label, _ in result]
    assert labels == ["POSITIVE", "NEGATIVE", "POSITIVE"]


def test_classify_returns_python_float_scores_in_unit_interval():
    result = classify(["Helpful guide.", "Broken response."])
    assert result is not None, "classify returned None: did you forget to return the list?"
    assert len(result) == 2
    for label, score in result:
        assert isinstance(label, str)
        assert type(score) is float, "score must be a built-in Python float, not a tensor"
        assert 0.0 <= score <= 1.0


def test_classify_matches_pipeline_built_from_same_objects():
    texts = [
        "Fast and helpful answer, solved my bug!",
        "The bot kept repeating the wrong link.",
        "Thanks, that worked after I restarted.",
    ]
    result = classify(texts)
    assert result is not None, "classify returned None: did you forget to return the list?"
    clf = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    expected = [(item["label"], round(item["score"], 3)) for item in clf(texts)]
    assert result == expected


def test_negatives_filters_by_threshold_and_preserves_order():
    texts = [
        "Helpful answer.",
        "san pham dung duoc nhung hoi cham",
        "The bot kept repeating the wrong link.",
        "Too slow and kept looping on the same error.",
    ]
    # Unaccented Vietnamese scores NEGATIVE ~0.696; the last two score ~0.999-1.0
    result = negatives(texts, threshold=0.9)
    assert result is not None, "negatives returned None: did you forget to return the list?"
    assert result == [
        "The bot kept repeating the wrong link.",
        "Too slow and kept looping on the same error.",
    ]


def test_empty_list_returns_empty_for_both_functions():
    cls_res = classify([])
    assert cls_res is not None, "classify([]) returned None instead of []"
    assert cls_res == []
    neg_res = negatives([], threshold=0.5)
    assert neg_res is not None, "negatives([]) returned None instead of []"
    assert neg_res == []
