import pytest
from exercise import hit_rates


def test_all_hits_return_one():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
        {"expected_source": "hours.md", "retrieved": ["pickup.md", "hours.md"]},
    ]
    assert hit_rates(results, ks=[2]) == {2: pytest.approx(1.0)}


def test_multiple_ks_and_rounding():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md", "hours.md"]},
        {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md", "hours.md"]},
        {"expected_source": "warranty.md", "retrieved": ["hours.md", "payment.md", "warranty.md"]},
    ]
    got = hit_rates(results, ks=[1, 2, 3])
    assert got == {
        1: pytest.approx(0.333),
        2: pytest.approx(0.667),
        3: pytest.approx(1.0),
    }


def test_skips_none_expected_source_from_denominator():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
        {"expected_source": "warranty.md", "retrieved": ["hours.md", "payment.md"]},
        {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
        {"expected_source": None, "retrieved": ["refunds.md", "loyalty.md"]},
    ]
    assert hit_rates(results, ks=[1, 2]) == {1: pytest.approx(0.5), 2: pytest.approx(0.5)}


@pytest.mark.parametrize(
    "results",
    [
        [],
        [{"expected_source": None, "retrieved": ["refunds.md"]}],
        [
            {"expected_source": None, "retrieved": ["a.md"]},
            {"expected_source": None, "retrieved": ["b.md"]},
        ],
    ],
)
def test_empty_or_all_none_returns_zero(results):
    assert hit_rates(results, ks=[1, 2]) == {1: pytest.approx(0.0), 2: pytest.approx(0.0)}


def test_empty_ks_returns_empty_dict():
    results = [{"expected_source": "a.md", "retrieved": ["a.md"]}]
    assert hit_rates(results, ks=[]) == {}


@pytest.mark.parametrize("bad_k", [0, -1])
def test_non_positive_k_raises_value_error(bad_k):
    results = [{"expected_source": "a.md", "retrieved": ["a.md"]}]
    with pytest.raises(ValueError):
        hit_rates(results, ks=[bad_k])
    with pytest.raises(ValueError):
        hit_rates(results, ks=[1, bad_k])
