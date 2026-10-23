from exercise import EchoModel, Model, Pipeline, ShoutModel


def test_pipeline_keeps_the_steps_it_is_given():
    steps = [EchoModel("e"), ShoutModel("s")]
    assert Pipeline(steps).steps == steps


def test_returns_the_text_unchanged_with_no_steps():
    assert Pipeline([]).run("hello") == "hello"


def test_one_step():
    assert Pipeline([EchoModel("e")]).run("hi") == "echo: hi"


def test_text_flows_from_one_step_to_the_next():
    pipe = Pipeline([ShoutModel("s"), EchoModel("e")])
    assert pipe.run("hi") == "echo: HI", "give each step the result of the previous one"


def test_order_of_steps_matters():
    pipe = Pipeline([EchoModel("e"), ShoutModel("s")])
    assert pipe.run("hi") == "ECHO: HI"


def test_add_puts_the_model_at_the_end():
    pipe = Pipeline([ShoutModel("s")])
    pipe.add(EchoModel("e"))
    assert pipe.run("hi") == "echo: HI"
    assert pipe.steps[-1].name == "e"


def test_add_works_on_an_empty_pipeline():
    pipe = Pipeline([])
    pipe.add(EchoModel("e"))
    assert pipe.run("yo") == "echo: yo"


def test_size_counts_the_steps():
    pipe = Pipeline([EchoModel("e"), ShoutModel("s")])
    assert pipe.size() == 2
    assert Pipeline([]).size() == 0


def test_size_grows_after_add():
    pipe = Pipeline([])
    pipe.add(EchoModel("e"))
    pipe.add(ShoutModel("s"))
    assert pipe.size() == 2


def test_a_pipeline_has_models_but_is_not_one():
    assert not isinstance(Pipeline([]), Model)
