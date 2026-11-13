import matplotlib.pyplot as plt
import pytest

from exercise import plot_loss


def test_sets_title_and_axis_labels():
    fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
    try:
        assert ax.get_title() == "Training loss"
        assert ax.get_xlabel() == "epoch"
        assert ax.get_ylabel() == "loss"
    finally:
        plt.close(fig)


def test_plots_one_line_with_expected_coordinates():
    fig, ax = plot_loss([1, 2, 3, 4], [0.85, 0.6, 0.42, 0.3])
    try:
        assert len(ax.lines) == 1, "draw exactly one line on ax"
        line = ax.lines[0]
        assert list(line.get_xdata()) == pytest.approx([1, 2, 3, 4])
        assert list(line.get_ydata()) == pytest.approx([0.85, 0.6, 0.42, 0.3])
    finally:
        plt.close(fig)


def test_uses_circle_marker():
    fig, ax = plot_loss([1, 2], [0.7, 0.4])
    try:
        assert len(ax.lines) == 1
        assert ax.lines[0].get_marker() == "o", "pass marker='o' to ax.plot()"
    finally:
        plt.close(fig)


def test_adds_legend_with_loss_label():
    fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
    try:
        legend = ax.get_legend()
        assert legend is not None, "call ax.legend() so the legend appears"
        texts = [t.get_text() for t in legend.get_texts()]
        assert texts == ["loss"]
    finally:
        plt.close(fig)


def test_creates_new_figure_on_each_call():
    fig1, ax1 = plot_loss([1, 2], [0.8, 0.4])
    fig2, ax2 = plot_loss([1, 2], [0.5, 0.2])
    try:
        assert fig1 is not fig2
        assert ax1 is not ax2
    finally:
        plt.close(fig1)
        plt.close(fig2)
