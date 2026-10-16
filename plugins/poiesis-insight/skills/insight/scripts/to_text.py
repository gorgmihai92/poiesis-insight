#!/usr/bin/env python3
"""Turn a data file into plain text Claude can read: tables to CSV, documents to TXT. Run with `python3 -I`.

  to_text.py responses.xlsx [--out DIR] [--mask]

- Tables: .csv and .tsv (normalized to CSV), .xlsx (one CSV per sheet), .xls (one CSV per sheet).
- Documents: .docx, .doc, .rtf, .odt (macOS `textutil` when present, else python-docx for .docx), .txt, .md.
- A Google Forms export is already CSV (Responses → Download, or File → Download → CSV in the linked sheet).

`--mask` replaces email addresses and phone numbers with placeholders in the output. Names and other identifying
columns still need to be removed or replaced by hand (see the skill). The original file is never changed.

Libraries for Excel and Word (openpyxl, xlrd, python-docx) are installed on first use into
~/.cache/poiesis-insight/pylib, not system-wide.
"""
import argparse
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

LIB = Path.home() / ".cache" / "poiesis-insight" / "pylib"
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
# Phone-like: optional +country code, digit groups separated by space, dot or dash; no "/" or ":" (dates, times).
PHONE = re.compile(r"(?<![\w/:.+-])(?:\+\d{1,3}[ .-]?)?\(?\d{2,4}\)?(?:[ .-]?\d{2,4}){2,4}(?![\w/:])")


def need(module: str, package: str):
    """Import a library, installing it into the private cache the first time."""
    sys.path.insert(0, str(LIB))
    try:
        return __import__(module)
    except ImportError:
        LIB.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--target", str(LIB), package], check=True)
        return __import__(module)


def _phone(m: re.Match) -> str:
    digits = sum(ch.isdigit() for ch in m.group(0))
    return "[phone]" if 9 <= digits <= 13 else m.group(0)


def mask(text: str) -> str:
    return PHONE.sub(_phone, EMAIL.sub("[email]", text))


def write_csv(rows, path: Path, masked: bool) -> int:
    n = 0
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for row in rows:
            cells = ["" if c is None else str(c) for c in row]
            w.writerow([mask(c) for c in cells] if masked else cells)
            n += 1
    return n


def tables(src: Path, out: Path, masked: bool) -> list[str]:
    ext = src.suffix.lower()
    done = []
    if ext in (".csv", ".tsv"):
        with src.open(newline="", encoding="utf-8-sig", errors="replace") as f:
            sample = f.read(4096)
            f.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
            dest = out / f"{src.stem}.csv"
            n = write_csv(csv.reader(f, dialect), dest, masked)
        done.append(f"{dest} ({n} rows)")
    elif ext == ".xlsx":
        openpyxl = need("openpyxl", "openpyxl")
        wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
        for ws in wb.worksheets:
            dest = out / f"{src.stem}.{re.sub(r'[^\w-]+', '_', ws.title)}.csv"
            n = write_csv(ws.iter_rows(values_only=True), dest, masked)
            done.append(f"{dest} ({n} rows)")
    elif ext == ".xls":
        xlrd = need("xlrd", "xlrd")
        wb = xlrd.open_workbook(str(src))
        for ws in wb.sheets():
            dest = out / f"{src.stem}.{re.sub(r'[^\w-]+', '_', ws.name)}.csv"
            n = write_csv((ws.row_values(i) for i in range(ws.nrows)), dest, masked)
            done.append(f"{dest} ({n} rows)")
    return done


def document(src: Path, out: Path, masked: bool) -> str:
    ext = src.suffix.lower()
    if ext in (".txt", ".md"):
        text = src.read_text(encoding="utf-8", errors="replace")
    elif shutil.which("textutil") and ext in (".docx", ".doc", ".rtf", ".odt"):
        text = subprocess.run(["textutil", "-convert", "txt", "-stdout", str(src)], capture_output=True, text=True, check=True).stdout
    elif ext == ".docx":
        docx = need("docx", "python-docx")
        d = docx.Document(str(src))
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            parts += ["\t".join(c.text for c in row.cells) for row in t.rows]
        text = "\n".join(parts)
    else:
        raise SystemExit(f"{src.suffix}: not supported here (convert to .docx, .txt or .csv first)")
    dest = out / f"{src.stem}.txt"
    dest.write_text(mask(text) if masked else text, encoding="utf-8")
    return f"{dest} ({len(text.splitlines())} lines)"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", type=Path)
    p.add_argument("--out", type=Path, help="folder for the output (default: next to the file)")
    p.add_argument("--mask", action="store_true", help="replace emails and phone numbers with placeholders")
    a = p.parse_args()
    src = a.file.resolve()
    out = (a.out or src.parent).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in (".csv", ".tsv", ".xlsx", ".xls"):
        for line in tables(src, out, a.mask):
            print(line)
    else:
        print(document(src, out, a.mask))
    return 0


if __name__ == "__main__":
    sys.exit(main())
