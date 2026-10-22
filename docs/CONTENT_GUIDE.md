# Content guide (lesson template)

Golden example: `curriculum/phase-01-python-core/p1-01-variables/`. Copy its shape.

## Folder layout

```
curriculum/<phase.dir>/<lesson-id>/          # lesson-id must be listed in curriculum/syllabus.yaml
  meta.yaml                                   # schema: tools/schema/meta.schema.json
  lesson.en.md  lesson.vi.md
  examples/NN_name.py + NN_name.out           # runnable, .out = exact expected stdout
  exercises/exNN-short-name/
    exercise.yaml                             # schema: tools/schema/exercise.schema.json
    prompt.en.md  prompt.vi.md
    starter.py                                # must FAIL the tests
    solution.py                               # must PASS the tests (hidden in UI until unlocked)
    test_exercise.py                          # imports the student's code as module `exercise`
  quiz.yaml                                   # schema: tools/schema/quiz.schema.json
```

IDs: lesson `p1-03-loops`, exercise `p1-03-ex01`, question `p1-03-q01`, flashcard `p1-03-f01`.
Tags must exist in `curriculum/topics.yaml`.

## Lesson markdown

- 5–10 minutes of reading for Track A beginners. Short paragraphs, one idea per section.
- Sections are `## 1. Title`, `## 2. ...`, ending with `## Recap` (VI: `## Tóm tắt`).
- Code fences use ```` ```python ````. Every python block must run on its own (the UI has a
  "Try it" button that sends the block to the editor). No `input()`, no network, no files in phase 1.
- Callouts: `> [!TIP]`, `> [!NOTE]`, `> [!WARNING]` (same callouts, same order in both languages).
- Tables are fine (GFM).
- **Code is never translated.** Between `lesson.en.md` and `lesson.vi.md`, code blocks must be
  identical except `#` comments. Strings inside code stay English.
- VI: natural Vietnamese, not word-for-word. Keep technical terms in English; on first use add the
  Vietnamese gloss, e.g. "vòng lặp (loop)", "**hàm** (function)".

## Exercises (2 per lesson, 3–6 tests each)

- `kind`: `code` (write it), `fill` (replace `___` blanks), `debug` (starter runs but has bugs),
  `project` (mini-project, more tests). Track A: mix at least one `fill` or `debug` per lesson.
- From lesson p1-02 on, give the learner a **function skeleton** and test the function with several
  inputs. Explain in the prompt: "write your code inside the function and `return` the answer".
- Starter should import cleanly where possible (`pass` / `return None` placeholders, blanks inside
  function bodies) so the learner sees per-test red/green rather than one crash.
  Exception: `fill` with module-level blanks and `debug` exercises may crash, that's fine.
- Tests use only: plain `assert`, `pytest.raises`, `pytest.approx`, `pytest.mark.parametrize`,
  and the `capsys` fixture. Nothing else (the browser runner implements only this subset).
- Test names read as sentences: `test_returns_zero_for_empty_list` (UI shows "returns zero for empty list").
- Hints: exactly 3 per language, escalating: (1) nudge / what to look at, (2) approach,
  (3) nearly the answer (a code shape, not the full solution).

## quiz.yaml

- 8 questions, at least one of each type: `mcq`, `output`, `fill`, `parsons`.
  - `mcq`: `answer` = index into `options` (options identical count in en/vi).
  - `output`: `code` + `answer` = exact stdout (the validator runs the code to check it).
  - `fill`: `code` with `___` blanks + `answer` list, one entry per blank (string or list of
    accepted strings). The validator fills the first accepted answer in and runs the code.
  - `parsons`: `lines` in the **correct** order (the UI shuffles). Must run as-is. Lines unique.
- Every question has `explanation` in both languages.
- 5 flashcards (front/back, both languages, optional `code`).

## Quality gate

```
uv run python tools/validate.py --path curriculum/<phase.dir>/<lesson-id>
uv run pytest curriculum
```

Both must be green before a lesson is "done".
