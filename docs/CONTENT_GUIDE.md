# Content guide (lesson template)

Golden example: `curriculum/phase-01-python-core/p1-01-variables/`. Copy its shape and its tone.
Audience: complete beginners (Track A) who want to become AI engineers. Vietnamese readers first.

## Folder layout

```
curriculum/<phase.dir>/<lesson-id>/          # lesson-id must be listed in curriculum/syllabus.yaml
  meta.yaml                                   # schema: tools/schema/meta.schema.json
  lesson.en.md  lesson.vi.md
  examples/NN_name.py                         # runnable
  examples/NN_name.out                        # exact expected stdout
  examples/NN_name.en.md  NN_name.vi.md       # '# Title' line + explanation (required)
  exercises/exNN-short-name/
    exercise.yaml                             # schema: tools/schema/exercise.schema.json
    prompt.en.md  prompt.vi.md
    starter.py                                # must FAIL the tests; shown prefilled in the editor
    solution.py                               # must PASS the tests (hidden until unlocked)
    test_exercise.py                          # imports the learner's code as module `exercise`
    alternatives/NN_approach.py               # other correct solutions, must PASS too
    alternatives/NN_approach.en.md  .vi.md    # '# Title' + why/when this approach
  quiz.yaml                                   # schema: tools/schema/quiz.schema.json
```

IDs: lesson `p1-03-loops`, exercise `p1-03-ex01`, question `p1-03-q01`, flashcard `p1-03-f01`.
Tags must exist in `curriculum/topics.yaml` (ask the lead to add one; do not edit shared files).

## Lesson markdown: clear, visual, beginner-friendly

Reading time 8–12 minutes. Short paragraphs (max 3 sentences), one idea per section.

Structure:

1. Opening paragraph (no heading): **why this matters**, ideally a concrete AI-engineering use
   ("Every chatbot reply is a string. Cleaning and formatting text is half the job.").
2. `## 1. ...`, `## 2. ...` concept sections. Each one follows the same rhythm:
   **idea in one sentence → analogy or mental model → smallest runnable code → what it prints
   (as a `#` comment) → one sentence on what to notice.**
3. `## N. Common mistakes` (VI: `## N. Lỗi thường gặp`): 2–4 real beginner errors, each with
   the wrong code, the error message or wrong output, and the fix.
4. `## Recap` (VI: `## Tóm tắt`): 4–6 bullets.

Make it **visual**. Every lesson needs at least **two** of these:

- A **mermaid diagram** (```` ```mermaid ````) for flow: decisions, loops, call order, pipelines.
  Rules: `flowchart TD` or `flowchart LR`; every label in double quotes (`A["x > 0?"]`);
  at most 10 nodes; no HTML, no `;`, no parentheses outside quotes. In `lesson.vi.md` translate
  the labels but keep the **same number of lines** (the validator compares line counts).
- A **trace table**: a markdown table showing how variables change step by step
  (`| step | i | total |`). Tables are the best way to show loops and accumulators.
- A **picture in text** inside a ```` ```text ```` fence, for example list indexes:
  ```
  index:   0      1      2
         ["a",   "b",   "c"]
  index:  -3     -2     -1
  ```
  Text fences are compared exactly between EN and VI, so keep them language-neutral.
- A **comparison table** (`| use this | when |`).

Every python block in the app has **Run** and **Visualize** buttons (Visualize steps through
the code and shows variables changing). Once per lesson, in the section with the most
interesting state change, invite the learner: "Press **Visualize** on this block and watch
`total` grow." (VI: "Bấm **Visualize** ở khối code này để xem `total` tăng dần.")

Callouts: `> [!TIP]`, `> [!NOTE]`, `> [!WARNING]` (same callouts, same order in both languages).

Code rules:
- ```` ```python ```` blocks must run on their own. No `input()`, no network. File I/O only from
  p1-09 on and only inside `tempfile.TemporaryDirectory()` (never write next to the lesson).
- Terminal commands go in ```` ```bash ```` fences (not runnable in the app; fine for phase 3 tools).
- Only use what has been taught (check the prerequisites in syllabus.yaml). If you need a
  built-in early (`len`, `round`, `sorted`), introduce it in one sentence where it first appears.
- **Code is never translated.** Between `lesson.en.md` and `lesson.vi.md`, code blocks must be
  identical except `#` comments. Strings inside code stay English.

Vietnamese: natural, friendly, not word-for-word (write it as a good Vietnamese teacher would
say it). Keep technical terms in English; on first use add the Vietnamese gloss, e.g.
"vòng lặp (loop)", "**hàm** (function)". Use "bạn" for the reader.

## Examples (2–3 per lesson)

Each example is a slightly bigger, realistic program (a receipt, a log summary, a data
cleaner) that combines the lesson's ideas. Its first line is a `#` comment summary.

`NN_name.en.md` / `NN_name.vi.md` (both required):

```markdown
# Shop receipt

**What it shows:** one sentence.

**Step by step**
1. Lines 2–4 create three variables ...
2. Line 6 ...

**Notice:** the one thing beginners usually miss here.

**Try it yourself:** one small change to make and what should happen.
```

## Exercises (2 per lesson, 3–6 tests each)

- `kind`: `code` (write it), `fill` (replace `___` blanks), `debug` (starter runs but has bugs),
  `project` (mini-project, more tests). Track A: at least one `fill` or `debug` per lesson.
- From p1-02 on, give a **function skeleton** in `starter.py`: signature, a docstring with one
  example call and its result, `# TODO` comments for the steps, and `return None` / `pass`.
  The starter is loaded into the editor automatically, so it must explain itself.
- Starter should import cleanly where possible so the learner sees per-test red/green.
  Exception: `fill` with module-level blanks and `debug` exercises may crash.
- `prompt.*.md`: the task in 2–4 sentences, then **Example** (input → output table or code),
  then **Rules** (bullets). Say "write your code inside the function and `return` the answer".
- Tests may use: plain `assert`, `pytest.raises`, `pytest.approx`, `pytest.mark.parametrize`,
  `pytest.fail`, the fixtures `capsys`, `tmp_path`, `caplog`, `monkeypatch`, and
  `@pytest.fixture` functions defined in the test file. Nothing else (the browser runner
  implements only this subset).
- Test names read as sentences: `test_returns_zero_for_empty_list` (UI shows "returns zero for
  empty list"). Add an assert message when the failure would otherwise confuse a beginner:
  `assert total == 6, "remember to add every number, not just the last one"`.

### Hints: they must actually get the learner unstuck

Exactly 3 per language, escalating:
1. **Point to the idea**: name the concept and the lesson section, and restate what the function
   must return for one concrete input. ("This is the accumulator pattern from §3. For
   `[1, 2, 3]` you must return `6`.")
2. **Give the plan**: the steps in plain words, in order, as a short numbered list.
3. **Show the shape**: a code skeleton in a python fence with the structure filled in and only
   one or two small `...` gaps. A learner who read the lesson must be able to finish in a minute.
   Never the full solution.

### Alternative solutions

Every `code` and `project` exercise needs at least one file in `alternatives/` (`fill`/`debug`
optional): a genuinely different correct approach (a loop vs. a built-in, `if` chain vs. dict
lookup, ...). The `.md` explains in 2–4 sentences how it works and when it is the better or
worse choice. It may preview a later topic if the `.md` says so. It must pass the tests.

## quiz.yaml: a question bank

- **15–18 questions**, at least **two** of each type: `mcq`, `output`, `fill`, `parsons`.
  The app draws 10 per attempt and shuffles questions and options every time.
  Mix difficulty: about 5 easy (1), 7 medium (2), 3 hard (3).
- `mcq`: `answer` = index into `options` (same count in en/vi). Options are shuffled, so never
  write "All of the above", "Both A and B" or anything that depends on position. If a question
  really needs a fixed order, add `shuffle_options: false`. Distractors are real misconceptions.
- `output`: `code` + `answer` = exact stdout (the validator runs the code to check it).
- `fill`: `code` with `___` blanks + `answer` list, one entry per blank (string or list of
  accepted strings). The validator fills the first accepted answer in and runs the code.
- `parsons`: `lines` in the **correct** order (the UI shuffles). Must run as-is. Lines unique.
  Make sure only one order is correct (dependencies between lines, or a printed result).
- Every question has an `explanation` in both languages that says **why**, not just the answer.
- 6 flashcards (front/back, both languages, optional `code`).

## Quality gate

```
uv run python tools/validate.py --path curriculum/<phase.dir>/<lesson-id>
uv run pytest curriculum
```

Both must be green before a lesson is "done".
