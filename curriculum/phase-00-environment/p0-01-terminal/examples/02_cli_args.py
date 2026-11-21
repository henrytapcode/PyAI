def run_cli(tokens: list[str]) -> int:
    if not tokens:
        print("Error: missing script name")
        return 1

    script = tokens[0]
    args = tokens[1:]
    if not script.endswith(".py"):
        print(f"Error: {script} is not a .py file")
        return 2

    print(f"Running {script} with args={args}")
    return 0


for sample in [
    ["train.py", "--epochs", "5"],
    ["notes.txt"],
    [],
]:
    code = run_cli(sample)
    print(f"exit code: {code}")
