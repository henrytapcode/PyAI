import matplotlib.pyplot as plt


def plot_loss(epochs: list[int], losses: list[float]) -> tuple:
    """Plot training loss over epochs and return (fig, ax).

    Example: fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
    """
    fig, ax = plt.subplots()
    ax.plot(epochs, losses, label="loss", marker="o")
    ax.set_title("Training loss")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.legend()
    return fig, ax
