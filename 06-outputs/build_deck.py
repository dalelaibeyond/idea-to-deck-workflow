#!/usr/bin/env python3
"""Idea-to-Deck Phase 5A: thin shell around the 10-tools/render engine.

S1 contract: data source = independent slides_data.json (B3a). It does not
depend on S2 design frontmatter or S3 deck-content parsing.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "10-tools"))

from render import build_pptx

OUT_DIR = Path(__file__).resolve().parent
SLIDES_DATA = OUT_DIR / "slides_data.json"
REGISTRY = ROOT / "10-tools" / "render" / "registry.json"
TOTAL_SLIDES = 6


def main():
    slides_data = json.loads(SLIDES_DATA.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    build_pptx(slides_data, registry, OUT_DIR / "presentation.pptx",
               total_slides=TOTAL_SLIDES)


if __name__ == "__main__":
    main()