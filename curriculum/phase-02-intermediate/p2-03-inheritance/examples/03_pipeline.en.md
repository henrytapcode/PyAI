# A pipeline of models

**What it shows:** composition. A `Pipeline` is not a model; it has a list of models and runs text through them in order.

**Step by step**
1. Lines 2-26 define the family: a base `Model` and three children (`EchoModel`, `ShoutModel`, `TagModel`).
2. Lines 29-31 define `Pipeline`. Its `__init__` just stores the list in `self.steps`. It does not inherit from anything.
3. Lines 33-34: `add` puts one more model at the end of the list.
4. Lines 36-40: `run` sends the text through each step. The output of one step becomes the input of the next, and a line is printed after each step.
5. Lines 43-48 build a pipeline with two steps, add a third, run it, and show that the pipeline is not a `Model`.

**Notice:** the last line prints `False`. A `Pipeline` has models but is not one, so `isinstance` says no.

**Try it yourself:** move the `TagModel` to the front of the list in line 43 (and remove the `add` line). The output changes without writing any new class.
