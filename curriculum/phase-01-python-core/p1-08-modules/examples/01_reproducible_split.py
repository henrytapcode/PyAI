# Split a tiny dataset into train/test in a reproducible way.
import random
import statistics as st

scores = [72, 85, 90, 66, 78, 95, 88, 70, 81, 60]


def split_scores(values, test_size, seed):
    rng = random.Random(seed)      # its own random generator with a fixed seed
    shuffled = list(values)        # copy, so the original stays untouched
    rng.shuffle(shuffled)
    test = shuffled[:test_size]
    train = shuffled[test_size:]
    return train, test


train, test = split_scores(scores, 3, seed=42)
again_train, again_test = split_scores(scores, 3, seed=42)

print("train:", train)
print("test: ", test)
print("same split twice:", test == again_test)
print("train mean:", round(st.mean(train), 2))
print("test mean: ", round(st.mean(test), 2))
print("stdev of all:", round(st.stdev(scores), 2))
