#!/usr/bin/env python3
"""Idea-to-Deck Phase 5A: thin shell around the 10-tools/render engine.

S3 (B3b) data source: design.md frontmatter + deck-content.md, compiled.
Preflight gates (fail-fast, no partial output):
  1. validate_design.py  — design frontmatter schema + engine cross-checks
  2. parse_deck.py       — deck-content A4 contract
  3. compile.py          — three-source consistency (A1/A3 single source)
slides_data.json is re-emitted as a compiled debug artifact (C3).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "10-tools"))

from render import build_pptx
from render.compile import compile_slides, load_frontmatter
from render.parse_deck import parse_deck
from render.validate_design import main as validate_design_main

OUT_DIR = Path(__file__).resolve().parent
DESIGN = OUT_DIR / "design.md"
DECK = OUT_DIR / "deck-content.md"
REGISTRY = ROOT / "10-tools" / "render" / "registry.json"


def main():
    if validate_design_main([str(DESIGN)]) != 0:
        return 1
    try:
        deck = parse_deck(DECK)
        slides = compile_slides(load_frontmatter(DESIGN), deck)
    except Exception as e:  # DeckError / CompileError share fail-fast contract
        print("PREFLIGHT FAIL {}".format(e))
        return 1

    (OUT_DIR / "slides_data.json").write_text(
        json.dumps(slides, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    build_pptx(slides, registry, OUT_DIR / "presentation.pptx")


if __name__ == "__main__":
    sys.exit(main())
