#!/usr/bin/env python3
"""C2 post-build consistency: rendered artifacts vs deck-content.md.

Usage:
    python postcheck.py [--deck P] [--design P] [--pptx P] [--html P]
                        [--skip-pptx] [--skip-html]

Checks (exit 0 == consistent, 1 == drift):
1. PPTX: per slide, the set of on-slide text strings (bullet glyphs and
   whitespace normalized) equals the compiled deck-content field set;
   speaker notes equal the compiled [Voiceover]/[Delivery Mindset]
   template exactly.
2. HTML: slide count equals deck total_slides; every compiled field
   string is present in the matching <section> text (the generator's
   entity escaping and the cover-meta pipe separator are modeled by
   reversing them before comparison).
"""

import argparse
import sys
from pathlib import Path

from pptx import Presentation

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent
REPO = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from render.compile import compile_slides, load_frontmatter  # noqa: E402
from render.parse_deck import parse_deck  # noqa: E402
from render.verify import _html_sections, _norm_text  # noqa: E402

BULLET_PREFIX = "\u2022"


def _expected_strings(slide):
    args = slide["args"]
    out = [_norm_text(args["title"])]
    kind = slide["type"]
    if kind == "HERO_CENTER":
        out += [_norm_text(args[k]) for k in ("kicker", "subtitle", "takeaway", "meta")]
    elif kind == "SPLIT_50_50":
        out.append(_norm_text(args["left_anchor"]))
        out += [_norm_text(i) for i in args["right_bullets"]]
    elif kind == "METRIC_HERO_ROW":
        for m in args["metrics"]:
            out += [_norm_text(m[k]) for k in ("number", "label", "context")]
    elif kind == "CARD_ROW_3":
        for c in args["cards"]:
            out.append(_norm_text(c["header"]))
            out += [_norm_text(i) for i in c["bullets"]]
    elif kind == "GRID_2X2":
        for q in args["quadrants"]:
            out.append(_norm_text(q["title"]))
            out += [_norm_text(i) for i in q["bullets"]]
    elif kind == "PROCESS_TIMELINE":
        for s in args["steps"]:
            out += [_norm_text(s[k]) for k in ("header", "summary")]
    return [s for s in out if s]


def _pptx_slide_strings(slide):
    got = []
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for line in shape.text_frame.text.split("\n"):
            if line.startswith(BULLET_PREFIX):
                line = line.lstrip(BULLET_PREFIX)
            s = _norm_text(line)
            if s:
                got.append(s)
    return got


def _unescape_html(fragment):
    for src, dst in (("&lt;", "<"), ("&gt;", ">"), ("&nbsp;", " "), ("&amp;", "&")):
        fragment = fragment.replace(src, dst)
    return fragment


def check_pptx(pptx_path, slides):
    problems = []
    prs = Presentation(str(pptx_path))
    if len(prs.slides) != len(slides):
        return ["pptx slide count {} != deck {}".format(len(prs.slides), len(slides))]
    for i, (pslide, slide) in enumerate(zip(prs.slides, slides), 1):
        expected = _expected_strings(slide)
        got = _pptx_slide_strings(pslide)
        missing = sorted(set(expected) - set(got))
        extra = sorted(set(got) - set(expected))
        if missing:
            problems.append("pptx slide {}: missing on-slide text: {}".format(i, missing))
        if extra:
            problems.append("pptx slide {}: unexpected on-slide text: {}".format(i, extra))
        want_notes = "[Voiceover]\n{}\n\n[Delivery Mindset]\n{}".format(
            slide["voiceover"], slide["mindset"])
        got_notes = pslide.notes_slide.notes_text_frame.text
        if got_notes != want_notes:
            problems.append("pptx slide {}: speaker notes differ from deck-content".format(i))
    return problems


def check_html(html_path, slides, total):
    problems = []
    sections = _html_sections(Path(html_path).read_text(encoding="utf-8"))
    if len(sections) != total:
        return ["html slide count {} != deck {}".format(len(sections), total)]
    for i, (section, slide) in enumerate(zip(sections, slides), 1):
        text = _norm_text(_unescape_html(section))
        for want in _expected_strings(slide):
            if want not in text:
                problems.append(
                    "html section {}: missing on-slide text: {!r}".format(i, want[:80]))
    return problems


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deck", default=str(REPO / "06-outputs" / "deck-content.md"))
    ap.add_argument("--design", default=str(REPO / "06-outputs" / "design.md"))
    ap.add_argument("--pptx", default=str(REPO / "06-outputs" / "presentation.pptx"))
    ap.add_argument("--html", default=str(REPO / "06-outputs" / "presentation.html"))
    ap.add_argument("--skip-pptx", action="store_true")
    ap.add_argument("--skip-html", action="store_true")
    args = ap.parse_args(argv)

    try:
        slides = compile_slides(load_frontmatter(args.design), parse_deck(args.deck))
    except Exception as e:
        print("PREFLIGHT FAIL {}".format(e))
        return 1

    problems = []
    if not args.skip_pptx:
        problems += check_pptx(args.pptx, slides)
    if not args.skip_html:
        problems += check_html(args.html, slides, len(slides))

    if problems:
        for p in problems:
            print("DRIFT {}".format(p))
        print("POSTCHECK FAIL ({})".format(len(problems)))
        return 1
    print("POSTCHECK OK pptx={} html={} ({} slides, all fields round-trip)".format(
        not args.skip_pptx, not args.skip_html, len(slides)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
