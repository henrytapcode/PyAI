A `Pipeline` runs text through a list of models, one after another. It is built by composition: it **has** models, it is not a model. The models are already written for you. Replace each `___` in `Pipeline` with the right code.

**Example**

```python
pipe = Pipeline([ShoutModel("s"), EchoModel("e")])
pipe.run("hi")     # "echo: HI"  ("hi" -> "HI" -> "echo: HI")
pipe.size()        # 2
```

**Rules**
- `Pipeline(steps)` keeps the list in `self.steps`.
- `add(model)` puts the model at the **end** of `self.steps`.
- `run(text)` gives the text to the first step's `generate`, gives that result to the next step, and so on. It returns the final text. With no steps it returns the text unchanged.
- `size()` returns how many steps the pipeline has.
- `Pipeline` stays a separate class: do not make it inherit from `Model`.

Press **Check** to run the tests.
