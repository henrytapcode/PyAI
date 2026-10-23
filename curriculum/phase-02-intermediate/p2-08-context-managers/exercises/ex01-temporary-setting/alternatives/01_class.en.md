# A class with `__enter__` and `__exit__`

The same behaviour written as a class (§3). `__enter__` remembers the old value and sets the new one, and `__exit__` puts things back and returns `False` so errors are not hidden. The small function at the end only exists so the tests can call `temporary_setting(...)` as before. It is longer than the generator, but it is the better choice when the manager must keep extra state that you read later.
