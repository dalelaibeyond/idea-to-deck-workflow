#!/usr/bin/env python3
"""Full-chain acceptance: deck-content -> compile -> render -> postcheck (C2).

Usage:
    python test_fullchain.py

Runs the complete S3 acceptance over the synthetic fixtures:
  deck-en.md (all 6 archetypes) and deck-zh.md (zh-CN CJK stress):
  1. compile (three-source gate)          2. PPTX render (python-pptx)
  3. Marp md generation + HTML render     4. postcheck round-trip (C2)
Plus one negative: mismatched deck/artifact pair must be caught.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent.parent
sys.path.insert(0, str(TOOLS))

from render import build_pptx  # noqa: E402
from render.compile import compile_slides, load_frontmatter  # noqa: E402
from render.marp.build_marp import main as build_marp_main  # noqa: E402
from render.parse_deck import parse_deck  # noqa: E402
from render.postcheck import main as postcheck_main  # noqa: E402

FIX = HERE / "fixtures"


def compile_fixture(deck_name, design_name):
    deck = parse_deck(FIX / deck_name)
    return compile_slides(load_frontmatter(FIX / design_name), deck)


def run_chain(tag, deck_name, design_name):
    slides = compile_fixture(deck_name, design_name)
    assert len(slides) >= 1

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pptx = tmp / "{}.pptx".format(tag)
        import json
        registry = json.loads((TOOLS / "render" / "registry.json").read_text(encoding="utf-8"))
        build_pptx(slides, registry, pptx, total_slides=len(slides))

        md = tmp / "{}.md".format(tag)
        html = tmp / "{}.html".format(tag)
        rc = build_marp_main(["--deck", str(FIX / deck_name),
                              "--design", str(FIX / design_name),
                              "--out-md", str(md), "--out-html", str(html)])
        assert rc == 0, "marp build failed for {}".format(tag)

        rc = postcheck_main(["--deck", str(FIX / deck_name),
                             "--design", str(FIX / design_name),
                             "--pptx", str(pptx), "--html", str(html)])
        assert rc == 0, "postcheck failed for {}".format(tag)
    print("PASS fullchain  {} ({} slides, pptx+html round-trip)".format(tag, len(slides)))


def run_negative():
    """en deck checked against zh render must be caught (count mismatch)."""
    slides = compile_fixture("deck-zh.md", "design-zh.md")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        pptx = tmp / "zh.pptx"
        import json
        registry = json.loads((TOOLS / "render" / "registry.json").read_text(encoding="utf-8"))
        build_pptx(slides, registry, pptx, total_slides=len(slides))
        rc = postcheck_main(["--deck", str(FIX / "deck-en.md"),
                             "--design", str(FIX / "design-en.md"),
                             "--pptx", str(pptx), "--skip-html"])
        assert rc == 1, "negative case passed unexpectedly"
    print("PASS negative  deck-en vs zh-render mismatch caught")


def main():
    run_chain("en", "deck-en.md", "design-en.md")
    run_chain("zh", "deck-zh.md", "design-zh.md")
    run_negative()
    print("ALL FULLCHAIN CASES PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
