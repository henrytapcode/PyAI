"""Zero-dependency HTML and PDF exporter for curriculum books, sheets, and exams."""

from __future__ import annotations

import argparse
import html
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

_FENCE_RE = re.compile(r"^```([a-zA-Z0-9_-]*)\s*$")
_HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$")
_CALLOUT_RE = re.compile(r"^>\s*\[!(NOTE|TIP|WARNING|CAUTION|IMPORTANT)\]\s*(.*)$")
_UL_RE = re.compile(r"^[-*]\s+(.+)$")
_OL_RE = re.compile(r"^\d+\.\s+(.+)$")
_HR_RE = re.compile(r"^---+\s*$")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")

_PRINT_CSS = """
@page {
  size: A4;
  margin: 16mm 14mm;
}
* {
  box-sizing: border-box;
}
body {
  font-family: "Be Vietnam Pro", "Segoe UI", system-ui, -apple-system, sans-serif;
  color: #111827;
  background: #ffffff;
  font-size: 10.5pt;
  line-height: 1.55;
  margin: 0;
  padding: 0;
}
h1, h2, h3, h4 {
  color: #0f172a;
  margin-top: 1.1em;
  margin-bottom: 0.45em;
  line-height: 1.25;
  break-after: avoid;
}
h1 { font-size: 20pt; border-bottom: 2px solid #0f172a; padding-bottom: 4pt; }
h2 { font-size: 14.5pt; border-bottom: 1px solid #cbd5e1; padding-bottom: 2pt; }
h3 { font-size: 12pt; }
h4 { font-size: 10.5pt; }
p { margin: 0.45em 0; }
ul, ol { margin: 0.4em 0 0.6em 1.4em; padding: 0; }
li { margin: 0.2em 0; }
code, pre {
  font-family: "JetBrains Mono", Consolas, "Courier New", monospace;
}
code {
  background: #f1f5f9;
  color: #0f172a;
  padding: 1pt 3.5pt;
  border-radius: 3pt;
  font-size: 9pt;
}
pre {
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-left: 3px solid #334155;
  border-radius: 4pt;
  padding: 8pt 10pt;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 8.8pt;
  line-height: 1.45;
  break-inside: avoid;
}
pre code {
  background: transparent;
  padding: 0;
  font-size: inherit;
}
pre.mermaid-src {
  border-left-color: #0369a1;
  background: #f0f9ff;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 0.7em 0;
  font-size: 9.2pt;
  break-inside: avoid;
}
th, td {
  border: 1px solid #cbd5e1;
  padding: 5pt 7pt;
  text-align: left;
  vertical-align: top;
}
th {
  background: #f1f5f9;
  font-weight: 700;
}
blockquote, .callout {
  border-left: 3.5px solid #0284c7;
  background: #f8fafc;
  padding: 7pt 10pt;
  margin: 0.65em 0;
  border-radius: 0 4pt 4pt 0;
  break-inside: avoid;
}
.callout-title {
  font-weight: 700;
  text-transform: uppercase;
  font-size: 8.5pt;
  letter-spacing: 0.04em;
  color: #0369a1;
  margin-bottom: 2pt;
}
.callout.warning, .callout.caution {
  border-left-color: #b45309;
  background: #fffbeb;
}
.callout.warning .callout-title, .callout.caution .callout-title {
  color: #b45309;
}
.cover {
  padding: 40mm 8mm 20mm;
  text-align: left;
  page-break-after: always;
}
.cover .eyebrow {
  font-size: 10pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #475569;
  font-weight: 700;
}
.cover h1 {
  font-size: 28pt;
  border: none;
  margin: 8pt 0 10pt;
}
.cover .subtitle {
  font-size: 12pt;
  color: #334155;
  max-width: 145mm;
}
.toc {
  page-break-after: always;
}
.toc-list {
  list-style: none;
  margin-left: 0;
}
.toc-list li {
  padding: 2pt 0;
  border-bottom: 1px dotted #e2e8f0;
}
.chapter-break {
  page-break-before: always;
}
.card, .question {
  border: 1px solid #cbd5e1;
  border-radius: 5pt;
  padding: 9pt 11pt;
  margin: 0.75em 0;
  break-inside: avoid;
}
.meta-row {
  font-size: 9pt;
  color: #475569;
  margin-bottom: 6pt;
}
.answer-box {
  border: 1px dashed #64748b;
  border-radius: 4pt;
  min-height: 28pt;
  padding: 6pt 8pt;
  margin-top: 6pt;
  color: #64748b;
  font-size: 8.5pt;
}
.options {
  list-style: none;
  margin: 0.4em 0 0 0;
}
.options li {
  padding: 2pt 0;
}
hr {
  border: none;
  border-top: 1px solid #cbd5e1;
  margin: 1em 0;
}
@media print {
  a { color: #0f172a; text-decoration: none; }
}
""".strip()

_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "book_eyebrow": "Python & AI Platform — Printable Textbook",
        "book_title": "Python to Production AI Engineering",
        "book_sub": (
            "Complete bilingual-aligned curriculum covering Python core, data, "
            "machine learning, deep learning, LLM/RAG agents, production APIs, and capstones."
        ),
        "toc": "Table of Contents",
        "outcomes": "Learning Outcomes",
        "examples": "Worked Examples",
        "output": "Expected Output",
        "exercises": "Exercises (Prompts Only)",
        "flashcards": "Key Flashcards",
        "front": "Concept",
        "back": "Takeaway",
        "cheatsheet": "Phase Cheat Sheet",
        "recap": "Lesson Recaps",
        "exam_sheet": "Printable Exam",
        "answer_key": "Answer Key & Explanations",
        "duration": "Duration",
        "minutes": "min",
        "pass_score": "Pass Score",
        "questions": "Questions",
        "write_answer": "Your answer:",
        "write_order": "Order (line numbers):",
        "answer_label": "Answer",
        "explanation_label": "Explanation",
        "capstone_title": "Capstones",
        "capstone_summary": (
            "End-to-end applied projects combining RAG, agents, and production APIs."
        ),
    },
    "vi": {
        "book_eyebrow": "Python & AI Platform — Giáo trình bản in",
        "book_title": "Python đến Kỹ thuật AI Production",
        "book_sub": (
            "Giáo trình đầy đủ từ Python cốt lõi, dữ liệu, machine learning, "
            "deep learning, LLM/RAG/agent, triển khai API tới các dự án capstone."
        ),
        "toc": "Mục lục",
        "outcomes": "Mục tiêu học tập",
        "examples": "Ví dụ minh họa",
        "output": "Kết quả mong đợi",
        "exercises": "Bài tập (Chỉ đề bài)",
        "flashcards": "Thẻ ghi nhớ trọng tâm",
        "front": "Khái niệm",
        "back": "Ghi nhớ",
        "cheatsheet": "Tờ tóm tắt Phase",
        "recap": "Tóm tắt bài học",
        "exam_sheet": "Đề thi bản in",
        "answer_key": "Đáp án & Giải thích",
        "duration": "Thời lượng",
        "minutes": "phút",
        "pass_score": "Điểm đạt",
        "questions": "Số câu hỏi",
        "write_answer": "Câu trả lời của bạn:",
        "write_order": "Thứ tự dòng:",
        "answer_label": "Đáp án",
        "explanation_label": "Giải thích",
        "capstone_title": "Capstone",
        "capstone_summary": "Các dự án ứng dụng hoàn chỉnh kết hợp RAG, agent và API production.",
    },
}


def _render_inline(text: str) -> str:
    """Escape HTML and format inline code, links, bold, and italic spans."""
    placeholders: list[str] = []

    def _stash_code(match: re.Match[str]) -> str:
        idx = len(placeholders)
        placeholders.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"\x00CODE{idx}\x00"

    def _stash_link(match: re.Match[str]) -> str:
        idx = len(placeholders)
        label = html.escape(match.group(1))
        href = html.escape(match.group(2), quote=True)
        placeholders.append(f'<a href="{href}">{label}</a>')
        return f"\x00CODE{idx}\x00"

    work = _INLINE_CODE_RE.sub(_stash_code, text)
    work = _LINK_RE.sub(_stash_link, work)
    escaped = html.escape(work)
    escaped = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _ITALIC_RE.sub(r"<em>\1</em>", escaped)
    for idx, snippet in enumerate(placeholders):
        escaped = escaped.replace(f"\x00CODE{idx}\x00", snippet)
    return escaped


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def _is_table_sep(line: str) -> bool:
    cells = _split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def render_markdown(text: str) -> str:
    """Convert Markdown text into sanitized, print-ready HTML."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        fence_match = _FENCE_RE.match(stripped)
        if fence_match:
            lang = fence_match.group(1).lower()
            code_lines: list[str] = []
            i += 1
            while i < n and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1
            cls = ' class="mermaid-src"' if lang == "mermaid" else ""
            body = html.escape("\n".join(code_lines))
            out.append(f"<pre{cls}><code>{body}</code></pre>")
            continue

        if _HR_RE.match(stripped):
            out.append("<hr />")
            i += 1
            continue

        head_match = _HEADING_RE.match(stripped)
        if head_match:
            level = len(head_match.group(1))
            out.append(f"<h{level}>{_render_inline(head_match.group(2))}</h{level}>")
            i += 1
            continue

        callout_match = _CALLOUT_RE.match(stripped)
        if callout_match:
            kind = callout_match.group(1).lower()
            first = callout_match.group(2).strip()
            parts = [first] if first else []
            i += 1
            while i < n and lines[i].lstrip().startswith(">"):
                parts.append(lines[i].lstrip()[1:].strip())
                i += 1
            inner = " ".join(p for p in parts if p)
            out.append(
                f'<div class="callout {kind}">'
                f'<div class="callout-title">{html.escape(kind)}</div>'
                f"<p>{_render_inline(inner)}</p></div>"
            )
            continue

        if stripped.startswith(">"):
            q_parts: list[str] = []
            while i < n and lines[i].lstrip().startswith(">"):
                q_parts.append(lines[i].lstrip()[1:].strip())
                i += 1
            out.append(f"<blockquote><p>{_render_inline(' '.join(q_parts))}</p></blockquote>")
            continue

        if "|" in line and i + 1 < n and _is_table_sep(lines[i + 1]):
            headers = _split_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_table_row(lines[i]))
                i += 1
            th_html = "".join(f"<th>{_render_inline(h)}</th>" for h in headers)
            tr_html = "".join(
                "<tr>" + "".join(f"<td>{_render_inline(c)}</td>" for c in row) + "</tr>"
                for row in rows
            )
            out.append(f"<table><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table>")
            continue

        if _UL_RE.match(stripped):
            items: list[str] = []
            while i < n and _UL_RE.match(lines[i].strip()):
                m = _UL_RE.match(lines[i].strip())
                if m:
                    items.append(f"<li>{_render_inline(m.group(1))}</li>")
                i += 1
            out.append(f"<ul>{''.join(items)}</ul>")
            continue

        if _OL_RE.match(stripped):
            items = []
            while i < n and _OL_RE.match(lines[i].strip()):
                m = _OL_RE.match(lines[i].strip())
                if m:
                    items.append(f"<li>{_render_inline(m.group(1))}</li>")
                i += 1
            out.append(f"<ol>{''.join(items)}</ol>")
            continue

        para_lines: list[str] = []
        while i < n:
            cur = lines[i]
            cur_s = cur.strip()
            if (
                not cur_s
                or _FENCE_RE.match(cur_s)
                or _HEADING_RE.match(cur_s)
                or _UL_RE.match(cur_s)
                or _OL_RE.match(cur_s)
                or _HR_RE.match(cur_s)
                or cur_s.startswith(">")
                or ("|" in cur and i + 1 < n and _is_table_sep(lines[i + 1]))
            ):
                break
            para_lines.append(cur_s)
            i += 1
        out.append(f"<p>{_render_inline(' '.join(para_lines))}</p>")

    return "\n".join(out)


def _wrap_document(title: str, lang: str, body_html: str) -> str:
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{html.escape(lang)}">\n'
        "<head>\n"
        '  <meta charset="utf-8" />\n'
        f"  <title>{html.escape(title)}</title>\n"
        f"  <style>{_PRINT_CSS}</style>\n"
        "</head>\n"
        f"<body>\n{body_html}\n</body>\n"
        "</html>\n"
    )


def _load_catalog(generated_dir: Path) -> dict[str, Any]:
    catalog_path = generated_dir / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError(
            f"Missing {catalog_path}. Run 'uv run python tools/build_content.py' first."
        )
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def _load_lesson(generated_dir: Path, lesson_id: str) -> dict[str, Any]:
    lesson_path = generated_dir / "lessons" / f"{lesson_id}.json"
    if not lesson_path.exists():
        raise FileNotFoundError(
            f"Missing {lesson_path}. Run 'uv run python tools/build_content.py' first."
        )
    return json.loads(lesson_path.read_text(encoding="utf-8"))


def find_browser(explicit: str | None = None) -> Path | None:
    """Locate Chrome, Chromium, or Edge binary for headless PDF printing."""
    if explicit:
        p = Path(explicit)
        return p if p.exists() else None

    for name in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge"):
        found = shutil.which(name)
        if found:
            return Path(found)

    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def html_to_pdf(html_path: Path, pdf_path: Path, browser: Path, timeout: int = 120) -> Path:
    """Render an HTML file to PDF using a headless Chromium-based browser."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    abs_pdf = pdf_path.resolve()
    cmd = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        html_path.resolve().as_uri(),
    ]
    subprocess.run(cmd, check=True, timeout=timeout, capture_output=True)
    if not abs_pdf.exists() or abs_pdf.stat().st_size == 0:
        raise RuntimeError(f"Browser finished without writing non-empty PDF: {abs_pdf}")
    return abs_pdf


def _iter_ready_groups(catalog: dict[str, Any]) -> list[tuple[str, str, list[dict[str, Any]]]]:
    groups: list[tuple[str, str, list[dict[str, Any]]]] = []
    for phase in catalog.get("phases", []):
        ready_lessons = [ls for ls in phase.get("lessons", []) if ls.get("ready")]
        if ready_lessons:
            groups.append((phase["id"], "phase", ready_lessons))
    caps = [c for c in catalog.get("capstones", []) if c.get("ready")]
    if caps:
        groups.append(("cap", "capstone", caps))
    return groups


def build_textbook_html(generated_dir: Path, lang: str) -> str:
    """Build a complete print-ready HTML textbook for all ready lessons."""
    catalog = _load_catalog(generated_dir)
    labels = _LABELS[lang]
    groups = _iter_ready_groups(catalog)
    phase_map = {p["id"]: p for p in catalog.get("phases", [])}

    toc_items: list[str] = []
    chapters_html: list[str] = []

    for group_id, group_kind, lessons in groups:
        if group_kind == "phase":
            group_title = phase_map[group_id]["title"][lang]
        else:
            group_title = labels["capstone_title"]
        toc_items.append(f"<li><strong>{html.escape(group_title)}</strong><ul>")
        for ls_entry in lessons:
            toc_items.append(
                f"<li>{html.escape(ls_entry['id'])} — {html.escape(ls_entry['title'][lang])}</li>"
            )
        toc_items.append("</ul></li>")

        for ls_entry in lessons:
            lesson = _load_lesson(generated_dir, ls_entry["id"])
            meta = lesson["meta"]
            title = meta["title"][lang]
            outcomes = meta.get("outcomes", {}).get(lang, [])
            body_md = lesson.get("body", {}).get(lang, "")

            parts = [
                '<section class="chapter-break">',
                f'<div class="meta-row">{html.escape(meta["id"])} | '
                f'{html.escape(group_title)} | {meta.get("duration_min", 0)} '
                f"{labels['minutes']}</div>",
                f"<h1>{html.escape(title)}</h1>",
            ]
            if outcomes:
                items = "".join(f"<li>{_render_inline(o)}</li>" for o in outcomes)
                parts.append(f"<h2>{labels['outcomes']}</h2><ul>{items}</ul>")
            parts.append(render_markdown(body_md))

            examples = lesson.get("examples", [])
            if examples:
                parts.append(f"<h2>{labels['examples']}</h2>")
                for ex in examples:
                    ex_title = ex["title"][lang]
                    parts.append(
                        f'<div class="card"><h3>{html.escape(ex_title)}</h3>'
                        f"<pre><code>{html.escape(ex.get('code', '').rstrip())}</code></pre>"
                        f"<p><strong>{labels['output']}:</strong></p>"
                        f"<pre><code>{html.escape(ex.get('output', '').rstrip())}</code></pre>"
                        "</div>"
                    )

            exercises = lesson.get("exercises", [])
            if exercises:
                parts.append(f"<h2>{labels['exercises']}</h2>")
                for ex in exercises:
                    ex_title = ex["title"][lang]
                    prompt_md = ex.get("prompt", {}).get(lang, "")
                    parts.append(
                        f'<div class="card"><h3>{html.escape(ex_title)}</h3>'
                        f"{render_markdown(prompt_md)}</div>"
                    )

            flashcards = lesson.get("quiz", {}).get("flashcards", [])
            if flashcards:
                parts.append(f"<h2>{labels['flashcards']}</h2>")
                rows = "".join(
                    "<tr>"
                    f"<td>{_render_inline(fc[lang]['front'])}</td>"
                    f"<td>{_render_inline(fc[lang]['back'])}</td>"
                    "</tr>"
                    for fc in flashcards
                )
                parts.append(
                    f"<table><thead><tr><th>{labels['front']}</th>"
                    f"<th>{labels['back']}</th></tr></thead><tbody>{rows}</tbody></table>"
                )
            parts.append("</section>")
            chapters_html.append("\n".join(parts))

    cover_html = (
        '<section class="cover">'
        f'<div class="eyebrow">{labels["book_eyebrow"]}</div>'
        f'<h1>{labels["book_title"]}</h1>'
        f'<p class="subtitle">{labels["book_sub"]}</p>'
        "</section>"
        '<section class="toc">'
        f"<h1>{labels['toc']}</h1>"
        f'<ul class="toc-list">{"".join(toc_items)}</ul>'
        "</section>"
    )
    return _wrap_document(labels["book_title"], lang, cover_html + "\n".join(chapters_html))


def _extract_recap_bullets(body_md: str) -> list[str]:
    """Extract bullet lines from ## Recap or ## Tóm tắt section if present."""
    lines = body_md.splitlines()
    in_recap = False
    bullets: list[str] = []
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            heading = s[3:].strip().lower()
            if heading in ("recap", "tóm tắt"):
                in_recap = True
                continue
            if in_recap:
                break
        elif in_recap:
            m = _UL_RE.match(s)
            if m:
                bullets.append(m.group(1))
    return bullets


def build_cheatsheet_html(generated_dir: Path, phase_id: str, lang: str) -> str:
    """Build a compact printable cheat sheet for a phase (`p1`..`p8` or `cap`)."""
    catalog = _load_catalog(generated_dir)
    labels = _LABELS[lang]

    if phase_id == "cap":
        phase_title = labels["capstone_title"]
        phase_summary = labels["capstone_summary"]
        lesson_entries = [c for c in catalog.get("capstones", []) if c.get("ready")]
    else:
        phase = next((p for p in catalog.get("phases", []) if p["id"] == phase_id), None)
        if phase is None:
            raise ValueError(f"Unknown phase_id: {phase_id}")
        phase_title = phase["title"][lang]
        phase_summary = phase["summary"][lang]
        lesson_entries = [ls for ls in phase.get("lessons", []) if ls.get("ready")]

    parts = [
        f'<div class="meta-row">{labels["cheatsheet"]} | {html.escape(phase_id.upper())}</div>',
        f"<h1>{html.escape(phase_title)}</h1>",
        f"<p>{_render_inline(phase_summary)}</p>",
    ]

    all_cards: list[tuple[str, str]] = []
    for entry in lesson_entries:
        lesson = _load_lesson(generated_dir, entry["id"])
        meta = lesson["meta"]
        outcomes = meta.get("outcomes", {}).get(lang, [])
        recap = _extract_recap_bullets(lesson.get("body", {}).get(lang, ""))
        if not recap:
            recap = [meta.get("summary", {}).get(lang, "")]

        parts.append(f'<div class="card"><h3>{html.escape(meta["title"][lang])}</h3>')
        if outcomes:
            out_li = "".join(f"<li>{_render_inline(o)}</li>" for o in outcomes)
            parts.append(f"<p><strong>{labels['outcomes']}:</strong></p><ul>{out_li}</ul>")
        recap_li = "".join(f"<li>{_render_inline(r)}</li>" for r in recap if r)
        if recap_li:
            parts.append(f"<p><strong>{labels['recap']}:</strong></p><ul>{recap_li}</ul>")
        parts.append("</div>")

        for fc in lesson.get("quiz", {}).get("flashcards", []):
            all_cards.append((fc[lang]["front"], fc[lang]["back"]))

    if all_cards:
        rows = "".join(
            f"<tr><td>{_render_inline(f)}</td><td>{_render_inline(b)}</td></tr>"
            for f, b in all_cards
        )
        parts.append(
            f"<h2>{labels['flashcards']}</h2>"
            f"<table><thead><tr><th>{labels['front']}</th>"
            f"<th>{labels['back']}</th></tr></thead><tbody>{rows}</tbody></table>"
        )

    return _wrap_document(f"{labels['cheatsheet']}: {phase_title}", lang, "\n".join(parts))


def _shuffle_parsons_lines(exam_id: str, q_id: str, lines: list[str]) -> list[str]:
    """Deterministically shuffle Parsons lines, avoiding canonical order when possible."""
    indices = list(range(len(lines)))
    rng = random.Random(f"{exam_id}:{q_id}")
    rng.shuffle(indices)
    if len(lines) > 1 and len(set(lines)) > 1:
        while [lines[i] for i in indices] == lines:
            rng.shuffle(indices)
    return [lines[i] for i in indices]


def build_exam_sheet_html(exam: dict[str, Any], lang: str) -> str:
    """Build a printable exam sheet with zero leaked answers or explanations."""
    labels = _LABELS[lang]
    title = exam["title"][lang]
    desc = exam["description"][lang]
    questions = exam.get("questions", [])
    pass_pct = int(round(float(exam.get("pass_score", 0.8)) * 100))

    parts = [
        f'<div class="meta-row">{labels["exam_sheet"]} | {html.escape(exam["id"])} | '
        f'{labels["duration"]}: {exam.get("duration_min", 0)} {labels["minutes"]} | '
        f'{labels["pass_score"]}: {pass_pct}% | '
        f'{labels["questions"]}: {len(questions)}</div>',
        f"<h1>{html.escape(title)}</h1>",
        f"<p>{_render_inline(desc)}</p>",
    ]

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for idx, q in enumerate(questions, 1):
        q_type = q["type"]
        q_lang = q[lang]
        parts.append(
            f'<div class="question">'
            f'<div class="meta-row">Q{idx} ({html.escape(q["id"])}) — '
            f"{html.escape(q_type.upper())}</div>"
            f"<p>{_render_inline(q_lang['prompt'])}</p>"
        )
        if q_type == "mcq":
            opts = "".join(
                f"<li><strong>{letters[i]}.</strong> {_render_inline(opt)}</li>"
                for i, opt in enumerate(q_lang.get("options", []))
            )
            parts.append(f'<ul class="options">{opts}</ul>')
        elif q_type in ("output", "fill"):
            parts.append(f"<pre><code>{html.escape(q.get('code', '').rstrip())}</code></pre>")
            parts.append(f'<div class="answer-box">{labels["write_answer"]}</div>')
        elif q_type == "parsons":
            shuffled = _shuffle_parsons_lines(exam["id"], q["id"], q.get("lines", []))
            numbered = "\n".join(f"{n}. {ln}" for n, ln in enumerate(shuffled, 1))
            parts.append(f"<pre><code>{html.escape(numbered)}</code></pre>")
            parts.append(f'<div class="answer-box">{labels["write_order"]}</div>')
        parts.append("</div>")

    return _wrap_document(f"{title} — {labels['exam_sheet']}", lang, "\n".join(parts))


def build_exam_answers_html(exam: dict[str, Any], lang: str) -> str:
    """Build a separate answer key and explanation sheet for an exam."""
    labels = _LABELS[lang]
    title = exam["title"][lang]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    parts = [
        f'<div class="meta-row">{labels["answer_key"]} | {html.escape(exam["id"])}</div>',
        f"<h1>{html.escape(title)} — {labels['answer_key']}</h1>",
    ]

    for idx, q in enumerate(exam.get("questions", []), 1):
        q_type = q["type"]
        q_lang = q[lang]
        ans = q.get("answer")
        if q_type == "mcq":
            opts = q_lang.get("options", [])
            ans_idx = int(ans)
            ans_text = opts[ans_idx] if 0 <= ans_idx < len(opts) else ""
            ans_html = (
                f"<p><strong>{labels['answer_label']}:</strong> "
                f"{letters[ans_idx]}. {_render_inline(ans_text)}</p>"
            )
        elif q_type == "output":
            ans_html = (
                f"<p><strong>{labels['answer_label']}:</strong></p>"
                f"<pre><code>{html.escape(str(ans))}</code></pre>"
            )
        elif q_type == "fill":
            blanks = ", ".join(f"<code>{html.escape(str(x))}</code>" for x in ans)
            ans_html = f"<p><strong>{labels['answer_label']}:</strong> {blanks}</p>"
        elif q_type == "parsons":
            lines = q.get("lines", [])
            order = ans if isinstance(ans, list) else list(range(len(lines)))
            ordered = "\n".join(lines[i] for i in order)
            ans_html = (
                f"<p><strong>{labels['answer_label']}:</strong></p>"
                f"<pre><code>{html.escape(ordered)}</code></pre>"
            )
        else:
            ans_html = f"<p><strong>{labels['answer_label']}:</strong> {html.escape(str(ans))}</p>"

        expl = q_lang.get("explanation", "")
        parts.append(
            f'<div class="card">'
            f'<div class="meta-row">Q{idx} ({html.escape(q["id"])}) — '
            f"{html.escape(q_type.upper())}</div>"
            f"{ans_html}"
            f"<p><strong>{labels['explanation_label']}:</strong> {_render_inline(expl)}</p>"
            "</div>"
        )

    return _wrap_document(f"{title} — {labels['answer_key']}", lang, "\n".join(parts))


def export_all(
    generated_dir: Path,
    out_dir: Path,
    only: str = "all",
    lang: str = "both",
    exam_id: str | None = None,
    phase_id: str | None = None,
    html_only: bool = False,
    browser_path: str | None = None,
) -> dict[str, list[Path]]:
    """Generate HTML and optional PDF artifacts into `out_dir`."""
    catalog = _load_catalog(generated_dir)
    langs = ["en", "vi"] if lang == "both" else [lang]

    browser: Path | None = None
    if not html_only:
        browser = find_browser(browser_path)
        if browser is None:
            raise RuntimeError(
                "No Chrome/Edge/Chromium executable found. Pass --html-only or --browser <path>."
            )

    html_dir = out_dir / "html"
    pdf_dir = out_dir / "pdf"
    html_dir.mkdir(parents=True, exist_ok=True)
    if not html_only:
        pdf_dir.mkdir(parents=True, exist_ok=True)

    written_html: list[Path] = []
    written_pdf: list[Path] = []

    def _emit(stem: str, doc_html: str) -> None:
        h_path = html_dir / f"{stem}.html"
        h_path.write_text(doc_html, encoding="utf-8")
        written_html.append(h_path)
        if not html_only and browser is not None:
            p_path = pdf_dir / f"{stem}.pdf"
            html_to_pdf(h_path, p_path, browser)
            written_pdf.append(p_path)

    if only in ("all", "book"):
        for ln in langs:
            _emit(f"pyai-textbook-{ln}", build_textbook_html(generated_dir, ln))

    if only in ("all", "sheets"):
        ready_phases = [
            p["id"]
            for p in catalog.get("phases", [])
            if any(ls.get("ready") for ls in p.get("lessons", []))
        ]
        if any(c.get("ready") for c in catalog.get("capstones", [])):
            ready_phases.append("cap")
        targets = [phase_id] if phase_id else ready_phases
        for pid in targets:
            for ln in langs:
                _emit(f"cheatsheet-{pid}-{ln}", build_cheatsheet_html(generated_dir, pid, ln))

    if only in ("all", "exams"):
        exam_entries = catalog.get("exams", [])
        if exam_id:
            exam_entries = [e for e in exam_entries if e["id"] == exam_id]
            if not exam_entries:
                raise ValueError(f"Unknown exam_id: {exam_id}")
        for entry in exam_entries:
            exam_data = json.loads(
                (generated_dir / "exams" / f"{entry['id']}.json").read_text(encoding="utf-8")
            )
            for ln in langs:
                _emit(f"exam-{entry['id']}-{ln}", build_exam_sheet_html(exam_data, ln))
                _emit(f"exam-{entry['id']}-{ln}-answers", build_exam_answers_html(exam_data, ln))

    return {"html": written_html, "pdf": written_pdf}


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export curriculum HTML and PDFs.")
    parser.add_argument("--generated-dir", type=Path, default=Path("apps/web/src/generated"))
    parser.add_argument("--out-dir", type=Path, default=Path("exports"))
    parser.add_argument("--only", choices=["all", "book", "sheets", "exams"], default="all")
    parser.add_argument("--lang", choices=["en", "vi", "both"], default="both")
    parser.add_argument("--exam", dest="exam_id", default=None)
    parser.add_argument("--phase", dest="phase_id", default=None)
    parser.add_argument("--html-only", action="store_true")
    parser.add_argument("--browser", default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    res = export_all(
        generated_dir=args.generated_dir,
        out_dir=args.out_dir,
        only=args.only,
        lang=args.lang,
        exam_id=args.exam_id,
        phase_id=args.phase_id,
        html_only=args.html_only,
        browser_path=args.browser,
    )
    print(f"Exported {len(res['html'])} HTML and {len(res['pdf'])} PDF files -> {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
