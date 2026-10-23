# Copy first, then sort in place

`scores[:]` is a slice with no limits, so it copies the whole list. Then `copy.sort(reverse=True)` sorts that copy in place, which leaves the original untouched. This is the same result as `sorted(scores, reverse=True)`, which does the copy and the sort in a single step. Use `sorted()` when you need a new list, and `.sort()` only when you are happy to change the list itself.
