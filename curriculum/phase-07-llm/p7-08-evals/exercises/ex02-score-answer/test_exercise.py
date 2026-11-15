import pytest
from exercise import score_grounded


def test_all_expected_facts_matched_and_grounded():
    ctx = "[1] Customer support hours are Monday to Friday, 9 AM to 6 PM."
    ans = "Customer support hours are Monday to Friday, 9 AM to 6 PM. [1]"
    res = score_grounded(ans, ["Monday to Friday", "9 AM to 6 PM"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == [1]
    assert res["bad_citations"] == []


def test_missing_one_of_two_facts_returns_half():
    ctx = "[1] Customer support hours are Monday to Friday, 9 AM to 6 PM."
    ans = "Customer support hours are Monday to Friday. [1]"
    res = score_grounded(ans, ["Monday to Friday", "9 AM to 6 PM"], ctx)
    assert res["facts"] == pytest.approx(0.5)
    assert res["faithful"] is True
    assert res["citations"] == [1]


def test_case_insensitive_facts_and_words():
    ctx = "[1] Refunds are issued within 30 days."
    ans = "REFUNDS ARE ISSUED WITHIN 30 DAYS. [1]"
    res = score_grounded(ans, ["30 Days"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == [1]


def test_unanswerable_idk_reply_passes_without_citations():
    ctx = "[1] Store pickup is ready 2 hours after order confirmation."
    ans = "I don't know based on the provided context."
    res = score_grounded(ans, [], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == []
    assert res["bad_citations"] == []


def test_unanswerable_non_idk_reply_scores_zero_facts():
    ctx = "[1] We accept Visa and Mastercard for orders."
    ans = "We accept Visa for orders. [1]"
    res = score_grounded(ans, [], ctx)
    assert res["facts"] == pytest.approx(0.0)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == [1]
    assert res["bad_citations"] == []


def test_fabricated_answer_flags_unique_unsupported_words_in_order():
    ctx = "[1] Refunds are issued within 30 days of purchase."
    ans = "Refunds take 30 days with free courier pickup and free courier tracking. [1]"
    res = score_grounded(ans, ["30 days"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is False
    assert res["unsupported"] == ["take", "with", "free", "courier", "pickup", "tracking"]
    assert res["citations"] == [1]
    assert res["bad_citations"] == []


def test_missing_citation_marks_answer_unfaithful():
    ctx = "[1] Refunds are issued within 30 days."
    ans = "Refunds are issued within 30 days."
    res = score_grounded(ans, ["30 days"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is False
    assert res["unsupported"] == []
    assert res["citations"] == []
    assert res["bad_citations"] == []


def test_bad_citation_number_flagged_and_unfaithful():
    ctx = "[1] Refunds are issued within 30 days.\n[2] Standard shipping arrives in 5 days."
    ans = "Refunds are issued within 30 days. [3]"
    res = score_grounded(ans, ["30 days"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is False
    assert res["unsupported"] == []
    assert res["citations"] == [3]
    assert res["bad_citations"] == [3]


def test_duplicate_citation_deduped_and_short_words_ignored():
    ctx = "[1] Refunds are issued within 30 days."
    ans = "Refunds are for you [1] within 30 days [1]."
    res = score_grounded(ans, ["30 days"], ctx)
    assert res["facts"] == pytest.approx(1.0)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == [1]
    assert res["bad_citations"] == []


def test_multiple_citations_keep_first_appearance_order_and_keep_facts_intact():
    ctx = "[1] Refunds take 30 days.\n[2] Express shipping arrives next day."
    facts = ["30 days", "receipt"]
    ans = "Express shipping arrives next day [2] and refunds take 30 days [1] [2]."
    res = score_grounded(ans, facts, ctx)
    assert facts == ["30 days", "receipt"]
    assert res["facts"] == pytest.approx(0.5)
    assert res["faithful"] is True
    assert res["unsupported"] == []
    assert res["citations"] == [2, 1]
    assert res["bad_citations"] == []
