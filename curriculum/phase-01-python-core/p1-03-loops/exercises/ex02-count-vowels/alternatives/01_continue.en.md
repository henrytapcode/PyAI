# Skip the consonants with continue

Here the `if` is flipped: when the letter is **not** a vowel, `continue` jumps to the next letter, and only vowels reach `count += 1`. Both versions give the same answer. The original is easier to read for a simple check like this; `continue` pays off when the loop body is long and you want to throw away unwanted items early.
