# Check build context and secrets with .dockerignore

**What it shows:** Filtering a realistic RAG service directory with `fnmatch` and `PurePosixPath` to shrink the Docker build context and verify that `.env` never leaks into an image.

**Step by step**
1. Lines 6–27 list 11 sample project paths (`PROJECT_FILES`) and a standard `.dockerignore` rule list (`SAFE_DOCKERIGNORE`).
2. Lines 30–43 define `is_ignored(rel_path, patterns)`, matching folder rules ending in `/` against path prefixes/parts and file wildcards with `fnmatch`.
3. Lines 46–54 split files into `included` and `excluded` lists via `audit_context`.
4. Lines 57–72 print which files reach the build context, which are skipped, and run a security check comparing `SAFE_DOCKERIGNORE` against a list missing `.env`.

**Notice:** `.env.example` stays in the build context while `.env` is blocked, showing how exact `.dockerignore` rules keep secrets out without hiding template files.

**Try it yourself:** Remove `"data/raw/"` from `SAFE_DOCKERIGNORE` and notice how `data/raw/handbook.pdf` immediately moves into the build context, bloating the image.
