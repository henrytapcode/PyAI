# Numeric slope estimation

Instead of plugging into explicit gradient formulas for `grad_w` and `grad_b`, this version estimates each slope directly from `mse` by nudging `w` and `b` up and down by a tiny step `h = 0.001`, just like §4 of the lesson. That means you only ever have to write the loss function itself, which works for any loss formula without deriving anything by hand. The trade-off is speed: every gradient descent step evaluates `mse` four extra times, which is fine for two parameters here but becomes too slow when a model has thousands or millions of weights.
