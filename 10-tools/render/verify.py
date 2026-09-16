#!/usr/bin/env python3
"""Content-level artifact verification for the idea-to-deck pipeline.

Usage:
    python verify.py --kind pptx --a A.pptx --b B.pptx
    python verify.py --kind html --a A.html --b B.html

- pptx: extracts every zip XML part and compares content hashes, ignoring
  zip entry metadata (python-pptx writes wall-clock mtimes into the archive).
- html: compares slide count and per-`<section>` normalized text, plus the
  theme CSS block (ignores Marp CLI version noise in the output head).

Exit code 0 == content identical, 1 == differ.
"""

import argparse
import hashlib
import re
import sys
import tempfile
import zipfile
from pathlib import Path

SECTION_RE = re.compile(r"<section[^>]*>(.*?)</section>", re.S)
STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)


def _part_hashes(pptx_path):
    with zipfile.ZipFile(pptx_path) as zf:
        parts = {}
        for name in zf.namelist():
            if name.endswith("/"):
                continue
            parts[name] = hashlib.sha1(zf.read(name)).hexdigest()
    return parts


def _norm_text(fragment):
    page_breaks = re.sub(r"--+|\*\*+|_+", " ", fragment)
    text = re.sub(r"<[^>]+>", " ", page_breaks)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _html_sections(html_text):
    sections = [s for s in SECTION_RE.findall(html_text)]
    return [_norm_text(s) for s in sections]


def compare_pptx(a, b):
    ha, hb = _part_hashes(a), _part_hashes(b)
    if ha == hb:
        return True, "identical: {} XML parts".format(len(ha))
    only_a = sorted(set(ha) - set(hb))
    only_b = sorted(set(hb) - set(ha))
    diffs = sorted(k for k in ha if k in hb and ha[k] != hb[k])
    lines = ["parts only in A ({}): {}".format(len(only_a), ", ".join(only_a) or "-"),
             "parts only in B ({}): {}".format(len(only_b), ", ".join(only_b) or "-"),
             "changed parts count: {}".format(len(diffs))]
    for k in diffs[:20]:
        lines.append("  CHANGED  {}  {} -> {}".format(k, ha[k][:8], hb[k][:8]))
    return False, "\n".join(lines)


def compare_html(a, b):
    ta, tb = Path(a).read_text(encoding="utf-8"), Path(b).read_text(encoding="utf-8")
    sa, sb = _html_sections(ta), _html_sections(tb)
    if sa == sb:
        ca = STYLE_RE.search(ta)
        cb = STYLE_RE.search(tb)
        css_ok = (ca and cb and ca.group(1) == cb.group(1)) or (ca is None and cb is None)
        if css_ok:
            return True, "identical: {} sections + theme CSS".format(len(sa))
        return False, "sections identical ({}), but theme CSS differs".format(len(sa))
    if len(sa) != len(sb):
        return False, "slide count differs: A={} B={}".format(len(sa), len(sb))
    for i, (x, y) in enumerate(zip(sa, sb), 1):
        if x != y:
            return False, "section {} differs:\n  A: {}\n  B: {}".format(i, x[:120], y[:120])
    return False, "unknown divergence"


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kind", choices=["pptx", "html"], default="pptx")
    ap.add_argument("--a", required=True, help="reference artifact")
    ap.add_argument("--b", required=True, help="candidate artifact")
    args = ap.parse_args(argv)

    ok, msg = (compare_pptx(args.a, args.b) if args.kind == "pptx"
               else compare_html(args.a, args.b))
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))