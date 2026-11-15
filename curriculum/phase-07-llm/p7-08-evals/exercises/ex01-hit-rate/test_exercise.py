import pytest
from exercise import hit_rate


def test_all_hits_return_one():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
        {"expected_source": "hours.md", "retrieved": ["pickup.md", "hours.md"]},
    ]
    assert hit_rate(results, k=2) == pytest.approx(1.0)


def test_half_hits_return_point_five():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
        {"expected_source": "warranty.md", "retrieved": ["hours.md", "payment.md"]},
    ]
    assert hit_rate(results, k=2) == pytest.approx(0.5)


def test_smaller_k_cuts_off_later_hit():
    results = [
        {"expected_source": "shipping.md", "retrieved": ["loyalty.md", "shipping.md"]},
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "hours.md"]},
    ]
    assert hit_rate(results, k=2) == pytest.approx(1.0)
    assert hit_rate(results, k=1) == pytest.approx(0.5)


def test_skips_none_expected_source_from_denominator():
    results = [
        {"expected_source": "refunds.md", "retrieved": ["refunds.md", "shipping.md"]},
        {"expected_source": "warranty.md", "retrieved": ["hours.md", "payment.md"]},
        {"expected_source": None, "retrieved": ["pickup.md", "payment.md"]},
        {"expected_source": None, "retrieved": ["refunds.md", "loyalty.md"]},
    ]
    assert hit_rate(results, k=2) == pytest.approx(0.5)


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
    assert hit_rate(results, k=2) == pytest.approx(0.0)
