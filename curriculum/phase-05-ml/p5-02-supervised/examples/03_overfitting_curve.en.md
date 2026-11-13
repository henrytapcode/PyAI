# Comparing underfit, good fit, and overfit curves

**What it shows:** Fitting polynomial models of degree `1`, `3`, and `6` on 8 noisy training points, printing both train and test MSE, and plotting all three curves alongside the train and test dots.

**Step by step**
1. Lines 5–7 generate 12 noisy points along a smooth arch for `x` in `[0, 1]`.
2. Lines 9–11 shuffle the indices with seed `27` and split `8` points for training and `4` for testing.
3. Lines 13–16 create a smooth `grid` of 100 points and plot the train and test scatter dots.
4. Lines 18–23 fit degrees `1`, `3`, and `6` using `np.polyfit` on `x_train` only, print `train_mse` and `test_mse`, and draw each curve with `np.polyval`.
5. Lines 25–30 add the title, axis labels, legend, and grid, then display the figure.

**Notice:** Degree `1` underfits (`test_mse = 0.283`), degree `3` hits the sweet spot (`test_mse = 0.018`), and degree `6` overfits badly (`train_mse = 0.004` yet `test_mse = 1.66`).

**Try it yourself:** Change `deg in [1, 3, 6]` to include degree `2` and check whether a parabola beats degree `3` on `test_mse`.
