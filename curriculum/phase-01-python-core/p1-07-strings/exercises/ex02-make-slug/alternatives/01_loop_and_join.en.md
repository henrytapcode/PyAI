# Lower each word in a loop

Here we split first, then loop over the words, lower-casing each one and collecting it in a new list before joining. `split()` already ignores spaces at the ends, so no `strip()` is needed. It is a bit longer, but it shows the accumulator pattern with strings. Lower-casing the whole text first, as in the solution, is shorter.
