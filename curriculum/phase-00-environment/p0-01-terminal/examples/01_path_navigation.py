from pathlib import PurePosixPath

cwd = PurePosixPath("/home/alex/projects/ai-app")
print("cwd:", cwd)
print("parent:", cwd.parent)
print("parts:", cwd.parts)

main_file = cwd / "src" / "main.py"
print("script:", main_file)
print("filename:", main_file.name)
print("suffix:", main_file.suffix)
print("is absolute:", main_file.is_absolute())
