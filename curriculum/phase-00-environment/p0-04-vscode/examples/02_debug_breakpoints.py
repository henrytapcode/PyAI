def buggy_first_passing(scores: list[int], passing: int) -> int | None:
    for idx, score in enumerate(scores):
        print(f"watch: idx={idx}, score={score}, check={score > passing}")
        if score > passing:
            return idx
    return None


def fixed_first_passing(scores: list[int], passing: int) -> int | None:
    for idx, score in enumerate(scores):
        if score >= passing:
            return idx
    return None


sample = [45, 70, 88]
print("buggy:", buggy_first_passing(sample, 70))
print("fixed:", fixed_first_passing(sample, 70))
