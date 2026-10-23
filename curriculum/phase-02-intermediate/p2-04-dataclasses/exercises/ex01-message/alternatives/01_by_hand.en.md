# Count and build by hand

This version counts the words with a loop (the accumulator pattern) and builds the dict by writing every key out. It does the same job as `len(...)` and `asdict`, but it is longer and you must remember to edit `to_dict` whenever you add a field. `asdict` also copes with fields that hold other dataclasses, so the solution is the better choice for real code. One more difference: `to_dict` here returns the very same `tags` list that the object holds, while `asdict` returns a copy, so changing the dict's list would also change the message.
