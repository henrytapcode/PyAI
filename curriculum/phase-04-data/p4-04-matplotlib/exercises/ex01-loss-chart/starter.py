import matplotlib.pyplot as plt


def plot_loss(epochs: list[int], losses: list[float]) -> tuple:
    """Plot training loss over epochs and return (fig, ax).

    Example: fig, ax = plot_loss([1, 2, 3], [0.9, 0.5, 0.3])
    """
    fig, ax = plt.___()
    ax.plot(epochs, losses, label="loss", marker=___)
    ax.set_title("Training loss")
    ax.___("epoch")
    ax.set_ylabel("loss")
    ax.___()
    return fig, ax
