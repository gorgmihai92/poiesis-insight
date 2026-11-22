#!/usr/bin/env python3
"""The entry gate of poiesis-insight: before an insight is built on a research note, each quote in the note is
looked for in the source's text. Run with `python3 -I`.

  quote_gate.py research/notes [more folders or .md files ...] [--papers research/papers] [--strict]

It reads what poiesis-research writes, and needs no other plugin:
- a quote is a list line that starts with a quotation mark and gives its page: `- "exact words" (p. 4)`;
- the source's text is a `.txt` file with a line `[p. N]` before each page: the file the note's **File** line
  names (with `.txt` in place of `.pdf`), or a file with the note's name in a --papers folder;
- the note's **Read** line says how much of the source was read.

One line per quote, and one per note that has nothing to check:

  FOUND       the words are in the source, starting on the page the note gives
  WRONG PAGE  the words are in the source, on another page
  NOT FOUND   the words are not in the source's text
  NO TEXT     the source's text is not on this machine, so the note's quotes were not checked
  NO QUOTES   the note has no quote line, so none of its claims can be checked this way
  NOT READ    a line under "Quotes" that could not be read as a quote

Letters and digits have to match in order, and so do the marks that change a number: a decimal point or comma
between digits, a minus or plus sign before one, and %, <, >, =, ±. Spaces, hyphens at line ends, quotation
marks, accents and ligatures are ignored, because text taken out of a PDF mangles them. `...` or `…` splits a
quote into parts that must all be there, in order, each within 200 letters of the one before. The words an
ellipsis skips are not checked (a "not" may be among them), so such a quote is marked "has an ellipsis: read the
source there". A quote may run onto the next page; it has to start on the page given. Any list line that starts
with a double quotation mark is read as a quote, wherever it is in the note.

A block of Obsidian properties at the very top of a note (YAML between a first line `---` and the next `---`) is
skipped: a list item in it that starts with a quotation mark is not a quote. Line numbers still count its lines.

A list line under a "Quotes" heading that cannot be read as a quote (no opening or closing quotation mark) is
reported as NOT READ, so that nothing is skipped in silence.

FOUND shows that the words are in the source. It does not show that a claim built on them follows.

Exit codes: 0 no quote failed; 1 a quote is NOT FOUND or on the WRONG PAGE, or with --strict a note could not
be checked (NO TEXT, NO QUOTES, NOT READ); 2 a wrong command line.
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

MARKS = "\"“”„«»"
QUOTE_LINE_RE = re.compile(r"^\s*[-*+]\s+[" + MARKS + r"](.+)$")
PAGE_RE = re.compile(r"\bpp?\.\s*(\d+)(?:\s*[-–—]\s*(\d+))?")
MARKER_RE = re.compile(r"^\[p\. (\d+)\]\s*$", re.M)
ELLIPSIS_RE = re.compile(r"\s*\[?(?:…|\.\.\.)\]?\s*")
FILE_LINE_RE = re.compile(r"^\s*[-*+]\s+\*\*File:?\*\*:?\s*`([^`]+)`", re.M)
READ_LINE_RE = re.compile(r"^\s*[-*+]\s+\*\*Read:?\*\*:?\s*(.+)$", re.M)
OLD_READ_RE = re.compile(r"\*\*((?:abstract|title|reference)[^*]*only[^*]*)\*\*", re.I)


NUMBER_MARKS = {"%", "<", ">", "=", "±"}
MINUS = {"-", "−", "–", "+"}
GAP = 200
QUOTES_HEADING_RE = re.compile(r"^#{1,6}\s+quotes?\b", re.I)
ANY_HEADING_RE = re.compile(r"^#{1,6}\s")
LIST_LINE_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\S")


def without_properties(text: str) -> str:
    """The text with a properties block at its top blanked line for line, so the line numbers stay the same. The
    block is Obsidian's: the first line is `---` and it ends at the next `---` line; never closed, it is not one."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip() != "---":
        return text
    end = next((i for i, line in enumerate(lines[1:], 1) if line.rstrip() == "---"), None)
    if end is None:
        return text
    return "".join(line[len(line.rstrip("\r\n")):] for line in lines[: end + 1]) + "".join(lines[end + 1:])


def fold(text: str) -> str:
    """What survives being taken out of a PDF: letters and digits in lower case, accents and ligatures undone,
    and the marks that change a number: a point or comma between digits, a sign before a digit, %, <, >, =, ±.
    A minus sign is kept as `-`."""
    chars = unicodedata.normalize("NFKD", text).casefold()
    out = []
    for i, char in enumerate(chars):
        before = chars[i - 1] if i else ""
        after = chars[i + 1] if i + 1 < len(chars) else ""
        if char.isalnum() and unicodedata.category(char) != "Mn":
            out.append(char)
        elif char in ".," and before.isdigit() and after.isdigit():
            out.append(char)
        elif char in MINUS and after.isdigit() and not before.isalnum():
            out.append("+" if char == "+" else "-")
        elif char in NUMBER_MARKS:
            out.append(char)
    return "".join(out)


def pages_of(text: str) -> dict[int, str]:
    """The folded text of each page. A text with no `[p. N]` line is one page, numbered 0."""
    marks = list(MARKER_RE.finditer(text))
    if not marks:
        return {0: fold(text)}
    return {int(mark.group(1)): fold(text[mark.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)])
            for i, mark in enumerate(marks)}


def quotes_of(note: str) -> list[tuple[int, str, tuple[int, int] | None]]:
    """(line number, the quoted words, the pages given or None) for each quote line."""
    found = []
    for number, line in enumerate(note.splitlines(), 1):
        hit = QUOTE_LINE_RE.match(line)
        if not hit:
            continue
        rest = hit.group(1)
        end = max(rest.rfind(mark) for mark in MARKS)
        if end <= 0:
            continue
        page = PAGE_RE.search(rest[end + 1:])
        span = (int(page.group(1)), int(page.group(2) or page.group(1))) if page else None
        found.append((number, rest[:end], span))
    return found


def unread_quote_lines(note: str, read: set[int]) -> list[tuple[int, str]]:
    """List lines under a "Quotes" heading that were not read as quotes."""
    found, inside = [], False
    for number, line in enumerate(note.splitlines(), 1):
        if ANY_HEADING_RE.match(line):
            inside = bool(QUOTES_HEADING_RE.match(line))
            continue
        if inside and number not in read and (LIST_LINE_RE.match(line) or line.lstrip().startswith(">")):
            found.append((number, line.strip()))
    return found


def read_level(note: str) -> str:
    """How much of the source was read, as the note says it; 'not stated' when it does not."""
    hit = READ_LINE_RE.search(note) or OLD_READ_RE.search(note)
    if not hit:
        return "not stated"
    level = hit.group(1).strip()
    return level if len(level) <= 60 else level[:57].rstrip() + "…"


def find(quote: str, pages: dict[int, str], span: tuple[int, int] | None) -> tuple[str, str]:
    """("FOUND" | "WRONG PAGE" | "NOT FOUND", where)."""
    parts = [part for part in (fold(piece) for piece in ELLIPSIS_RE.split(quote)) if part]
    if not parts:
        return "NOT FOUND", "nothing to look for"

    def start_in(text: str) -> int:
        start = text.find(parts[0])
        while start >= 0:
            position = start + len(parts[0])
            for part in parts[1:]:
                found = text.find(part, position, position + GAP + len(part))
                if found < 0:
                    break
                position = found + len(part)
            else:
                return start
            start = text.find(parts[0], start + 1)
        return -1

    numbers = sorted(pages)
    letters = sum(map(len, parts))
    weak = f" (only {letters} letters: a weak check)" if letters < 20 else ""
    if len(parts) > 1:
        weak += " (has an ellipsis: read the source there" + (", and a part is under 12 letters" if min(map(len, parts)) < 12 else "") + ")"
    if numbers == [0]:
        return ("FOUND", "the text has no page marks" + weak) if start_in(pages[0]) >= 0 \
            else ("NOT FOUND", "not in the source's text")
    if span:
        own = "".join(pages.get(number, "") for number in range(span[0], span[1] + 1))
        if 0 <= start_in(own + pages.get(span[1] + 1, "")) < len(own):
            return "FOUND", f"p. {span[0]}" + ("" if span[0] == span[1] else f"–{span[1]}") + weak
    whole = "".join(pages[number] for number in numbers)
    start = start_in(whole)
    if start < 0:
        return "NOT FOUND", "not in the source's text"
    seen = 0
    first = numbers[-1]
    for number in numbers:
        seen += len(pages[number])
        if start < seen:
            first = number
            break
    if span is None:
        return "FOUND", f"p. {first}; the note gives no page" + weak
    return "WRONG PAGE", f"the note says p. {span[0]}; the words start on p. {first}"


def source_text(note_path: Path, note: str, papers: list[Path]) -> Path | None:
    candidates = []
    named = FILE_LINE_RE.search(note)
    if named:
        target = (note_path.parent / named.group(1)).resolve()
        candidates += [target.with_suffix(".txt"), target]
    for folder in papers:
        candidates.append(folder / f"{note_path.stem}.txt")
        if named:
            candidates.append(folder / Path(named.group(1)).with_suffix(".txt").name)
    return next((path for path in candidates if path.suffix == ".txt" and path.is_file()), None)


def check(paths: list[Path], papers: list[Path], strict: bool) -> int:
    notes = sorted(path for given in paths for path in ([given] if given.is_file() else given.rglob("*.md")))
    counts: dict[str, int] = {}
    unchecked: list[str] = []

    def say(status: str, note: Path, detail: str) -> None:
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:10} {note.name} · {detail}")

    for path in notes:
        note = without_properties(path.read_text(encoding="utf-8-sig", errors="replace"))
        level = read_level(note)
        quotes = quotes_of(note)
        odd = unread_quote_lines(note, {number for number, _, _ in quotes})
        for number, line in odd:
            say("NOT READ", path, f"line {number} · under Quotes and not a quote line: {line[:60]}")
        if odd:
            unchecked.append(path.name)
        if not quotes:
            say("NO QUOTES", path, f"read: {level} · no quote line, so nothing was checked")
            unchecked.append(path.name)
            continue
        text = source_text(path, note, papers)
        if text is None:
            say("NO TEXT", path, f"read: {level} · {len(quotes)} quote{'' if len(quotes) == 1 else 's'} not "
                                 "checked: the source's text is not here")
            unchecked.append(path.name)
            continue
        pages = pages_of(text.read_text(encoding="utf-8", errors="replace"))
        for number, quote, span in quotes:
            status, where = find(quote, pages, span)
            shown = quote if len(quote) <= 70 else quote[:67] + "…"
            say(status, path, f"line {number} · {where} · \"{shown}\"")

    print()
    print(" · ".join(f"{status}: {count}" for status, count in sorted(counts.items())) or "No notes.")
    failed = counts.get("NOT FOUND", 0) + counts.get("WRONG PAGE", 0)
    if failed:
        print(f"{failed} quote{'' if failed == 1 else 's'} failed: do not build on those claims until the note is "
              "corrected.")
    if unchecked:
        print(f"{len(unchecked)} note{'' if len(unchecked) == 1 else 's'} not checked against the source: use "
              "their claims as unchecked and name them under \"Not checked\"."
              + (" With --strict this fails." if strict else ""))
    return 1 if failed or (strict and unchecked) else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", type=Path, help="notes: folders or .md files")
    parser.add_argument("--papers", type=Path, action="append", default=[],
                        help="where the sources' .txt files are, when they are not next to their PDF")
    parser.add_argument("--strict", action="store_true",
                        help="also fail when a note could not be checked (NO TEXT, NO QUOTES)")
    args = parser.parse_args(argv)
    missing = [str(path) for path in args.paths if not path.exists()]
    if missing:
        parser.error("not found: " + ", ".join(missing))
    return check(args.paths, args.papers, args.strict)


if __name__ == "__main__":
    sys.exit(main())
