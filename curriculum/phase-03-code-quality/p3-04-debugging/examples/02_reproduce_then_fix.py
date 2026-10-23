# Shrink a bug report to the smallest failing call, then fix it and keep the cases as tests.
def chunk(items, size):
    return [items[i : i + size] for i in range(0, len(items) - size + 1, size)]


# The report: "some documents go missing". Try smaller and smaller inputs.
print(chunk([1, 2, 3, 4], 2))
print(chunk([1, 2, 3], 2))
print(chunk([1], 2))


def chunk(items, size):
    return [items[i : i + size] for i in range(0, len(items), size)]


# The smallest failing cases become tests that must pass now.
assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
assert chunk([1, 2, 3], 2) == [[1, 2], [3]]
assert chunk([1], 2) == [[1]]
assert chunk([], 2) == []
print("all cases pass")
