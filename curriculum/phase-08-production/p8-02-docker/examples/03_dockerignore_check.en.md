# Check build context and secrets with .dockerignore

**What it shows:** Filtering a realistic RAG service directory from the build-context root using `fnmatchcase` and `split("/")` so nested caches like `rag/__pycache__` are excluded and `.env` never leaks into an image.

**Step by step**
1. Lines 5–26 list 11 sample project paths (`PROJECT_FILES`) and a root-relative `.dockerignore` rule list (`SAFE_DOCKERIGNORE`) using `**/__pycache__` and `**/*.pyc`.
2. Lines 29–50 define `_match_from` and `is_ignored(rel_path, patterns)`, matching each pattern segment from the context root (or at any depth when a rule starts with `**`), omitting `!` exception rules.
3. Lines 53–61 split files into `included` and `excluded` lists via `audit_context`.
4. Lines 64–79 print which files reach the build context, which are skipped, and run a security check comparing `SAFE_DOCKERIGNORE` against a list missing `.env`.

**Notice:** `.env.example` stays in the build context while `.env` is blocked, and `**/__pycache__` plus `**/*.pyc` catch nested files like `rag/__pycache__/retriever.cpython-313.pyc` that root-only `__pycache__/` or `*.pyc` rules would miss.

**Try it yourself:** Remove `"data/raw/"` from `SAFE_DOCKERIGNORE` and notice how `data/raw/handbook.pdf` immediately moves into the build context, bloating the image.
