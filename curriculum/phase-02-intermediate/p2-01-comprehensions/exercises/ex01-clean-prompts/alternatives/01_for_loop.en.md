# A plain for loop

This is the loop-and-`append` version from §1. It cleans the text first, then appends it only if something is left (an empty string counts as `False`). It is longer than the comprehension but easy to follow line by line, and it is the better choice if you later need to print, count, or `continue` inside the loop.
