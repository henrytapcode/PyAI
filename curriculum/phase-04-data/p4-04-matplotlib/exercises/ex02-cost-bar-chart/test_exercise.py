import matplotlib.pyplot as plt
import pandas as pd
import pytest

from exercise import cost_bar_chart


def test_aggregates_and_sorts_bars_descending():
    df = pd.DataFrame({
        "model": ["mini", "gpt-4o", "mini", "claude", "gpt-4o"],
        "cost": [0.15, 2.40, 0.25, 2.95, 1.85],
    })
    fig, ax = cost_bar_chart(df)
    try:
        heights = [float(p.get_height()) for p in ax.patches]
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["gpt-4o", "claude", "mini"], "sort models by total cost descending"
        assert heights == pytest.approx([4.25, 2.95, 0.40])
    finally:
        plt.close(fig)


def test_each_model_appears_once():
    df = pd.DataFrame({
        "model": ["a", "b", "a", "c", "b", "a"],
        "cost": [1.0, 2.0, 1.5, 0.5, 3.0, 0.5],
    })
    fig, ax = cost_bar_chart(df)
    try:
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert len(ax.patches) == 3, "sum duplicate models so each model has one bar"
        assert len(set(labels)) == 3
        assert labels == ["b", "a", "c"]
    finally:
        plt.close(fig)


def test_sets_title_and_ylabel():
    df = pd.DataFrame({
        "model": ["gpt-4o", "mini"],
        "cost": [3.0, 0.5],
    })
    fig, ax = cost_bar_chart(df)
    try:
        assert ax.get_title() == "Cost by model"
        assert ax.get_ylabel() == "cost (USD)"
    finally:
        plt.close(fig)


def test_handles_decimal_costs_across_different_models():
    df = pd.DataFrame({
        "model": ["haiku", "sonnet", "opus", "sonnet"],
        "cost": [0.12, 1.10, 4.50, 0.65],
    })
    fig, ax = cost_bar_chart(df)
    try:
        heights = [float(p.get_height()) for p in ax.patches]
        labels = [t.get_text() for t in ax.get_xticklabels()]
        assert labels == ["opus", "sonnet", "haiku"]
        assert heights == pytest.approx([4.50, 1.75, 0.12])
    finally:
        plt.close(fig)


def test_does_not_modify_input_dataframe():
    df = pd.DataFrame({
        "model": ["mini", "gpt-4o", "mini"],
        "cost": [0.2, 2.0, 0.3],
    })
    snapshot = df.to_dict("list")
    fig, _ax = cost_bar_chart(df)
    try:
        assert df.to_dict("list") == snapshot, "do not mutate the input DataFrame"
    finally:
        plt.close(fig)
