# A helper function and two steps

The cleaning rule gets its own named function, `normalize`, and the work is split into two short comprehensions: clean everything, then drop the empty strings. Each line reads like a sentence. It builds one extra list, which does not matter for small inputs. This style is the better one when the cleaning rule grows or is needed in other places.
