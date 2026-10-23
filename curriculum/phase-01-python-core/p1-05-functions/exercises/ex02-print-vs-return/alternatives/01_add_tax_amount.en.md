# Name each step

`area` stores the product in `result` before returning it, and `price_with_tax` computes the `tax` amount first and then adds it (`price + tax` is the same as `price * (1 + rate)`). `greet` joins the pieces with `+` instead of an f-string. All of these are correct; the f-string version is usually shorter and easier to read.
