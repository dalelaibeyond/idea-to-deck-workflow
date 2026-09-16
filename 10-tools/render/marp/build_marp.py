#!/usr/bin/env python3
"""Generate marp_deck.md from deck-content.md + design.md and render HTML (B4).

Single source chain: the same compiled slides that drive the PPTX path
drive the HTML path (A1). The CSS asset lives at
``10-tools/render/marp/marp-theme.css`` (D2 SOP: one class per archetype);
the generator embeds it into the generated frontmatter via the ``style:``
directive. Empirical note: ``--theme-set`` with a ``@base default`` theme
recompiles the CSS through sass and diverges from the golden CSS stack at
the theme block — the ``style:`` directive is the only injection mechanism
that reproduces it content-identically, so the todo's "--theme 注入" is
implemented as asset + directive injection. ``marp_deck.md`` is a compiled
artifact (C3), never hand-maintained.

Usage:
    python build_marp.py [--deck P] [--design P] [--out-md P] [--out-html P]
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # 10-tools/render/marp
TOOLS = HERE.parent.parent                      # 10-tools
REPO = TOOLS.parent                             # repo root
sys.path.insert(0, str(TOOLS))

from render.compile import compile_slides, load_frontmatter  # noqa: E402
from render.parse_deck import parse_deck  # noqa: E402

THEME_CSS = HERE / "marp-theme.css"


def _esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _meta(text):
    return _esc(text).replace("  |  ", " &nbsp;|&nbsp; ")


def _bullet(item):
    lead, sep, body = item.partition(":")
    if sep:
        return "    <li><b>{}:</b> {}</li>\n".format(_esc(lead), _esc(body.lstrip(" ")))
    return "    <li>{}</li>\n".format(_esc(item))


def _notes(slide):
    return "<!--\nVoiceover: {}\nDelivery Mindset: {}\n-->\n\n".format(
        slide["voiceover"], slide["mindset"])


def _hero(args):
    return ("# Slide 1\n"
            '<div class="hero">\n'
            '  <div class="band"></div>\n'
            '  <div class="tag">{}</div>\n'
            "  <h1>{}</h1>\n"
            '  <div class="subtitle">{}</div>\n'
            '  <div class="takeaway">{}</div>\n'
            '  <div class="meta">{}</div>\n'
            "</div>\n").format(_esc(args["kicker"]), _esc(args["title"]),
                               _esc(args["subtitle"]), _esc(args["takeaway"]),
                               _meta(args["meta"]))


def _split(args):
    lines = ['<div class="split">\n'
             '  <div class="left">{}</div>\n'
             '  <div class="right"><ul>\n'.format(_esc(args["left_anchor"]))]
    for item in args["right_bullets"]:
        lines.append(_bullet(item))
    lines.append("  </ul></div>\n</div>\n")
    return "".join(lines)


def _metrics(args):
    lines = ['<div class="metrics">\n']
    for metric in args["metrics"]:
        lines.append('  <div class="card">\n'
                     '    <div class="number">{}</div>\n'
                     '    <div class="label">{}</div>\n'
                     '    <div class="context">{}</div>\n'
                     "  </div>\n".format(_esc(metric["number"]),
                                         _esc(metric["label"]),
                                         _esc(metric["context"])))
    lines.append("</div>\n")
    return "".join(lines)


def _cards(args):
    lines = ['<div class="cards">\n']
    for i, card in enumerate(args["cards"]):
        cls = "card border-top" if i == 1 else "card"
        lines.append('  <div class="{}">\n    <h3>{}</h3>\n    <ul>\n'.format(
            cls, _esc(card["header"])))
        for item in card["bullets"]:
            lines.append("      <li>{}</li>\n".format(_esc(item)))
        lines.append("    </ul>\n  </div>\n")
    lines.append("</div>\n")
    return "".join(lines)


def _grid(args):
    lines = ['<div class="grid">\n']
    for i, quad in enumerate(args["quadrants"]):
        cls = "quad act" if i == 3 else "quad"
        lines.append('  <div class="{}">\n    <h3>{}</h3>\n    <ul>\n'.format(
            cls, _esc(quad["title"])))
        for item in quad["bullets"]:
            lines.append("      <li>{}</li>\n".format(_esc(item)))
        lines.append("    </ul>\n  </div>\n")
    lines.append("</div>\n")
    return "".join(lines)


def _timeline(args):
    # GAP-B4-1: PROCESS_TIMELINE has no archetype CSS in marp-theme.css
    # (V1.0 corpus never used it; adding CSS would drift the golden block).
    # Markup renders unstyled-but-valid until the first timeline deck goes
    # through Phase 4 HITL and evolves the CSS baseline.
    lines = ['<div class="timeline">\n']
    for step in args["steps"]:
        lines.append('  <div class="step">\n'
                     '    <div class="step-header">{}</div>\n'
                     '    <div class="step-summary">{}</div>\n'
                     "  </div>\n".format(_esc(step["header"]), _esc(step["summary"])))
    lines.append("</div>\n")
    return "".join(lines)


_BODIES = {
    "HERO_CENTER": _hero,
    "SPLIT_50_50": _split,
    "METRIC_HERO_ROW": _metrics,
    "CARD_ROW_3": _cards,
    "GRID_2X2": _grid,
    "PROCESS_TIMELINE": _timeline,
}


def render_markdown(slides, css):
    css_block = "".join("  {}\n".format(line) for line in css.rstrip("\n").split("\n"))
    head = "---\nmarp: true\ntheme: default\npaginate: true\nsize: 16:9\nstyle: |\n{}---\n\n".format(css_block)
    bodies = []
    for i, slide in enumerate(slides):
        if slide["type"] == "HERO_CENTER":
            body = _hero(slide["args"])
        else:
            body = ('<div class="topbar"></div>\n\n# {}\n\n{}').format(
                _esc(slide["args"]["title"]), _BODIES[slide["type"]](slide["args"]))
            if i == len(slides) - 1:
                body += '\n<div class="accentbar"></div>\n'
        bodies.append(_notes(slide) + body)
    return head + "\n---\n\n".join(bodies)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deck", default=str(REPO / "06-outputs" / "deck-content.md"))
    ap.add_argument("--design", default=str(REPO / "06-outputs" / "design.md"))
    ap.add_argument("--out-md", default=str(REPO / "06-outputs" / "marp_deck.md"))
    ap.add_argument("--out-html", default=str(REPO / "06-outputs" / "presentation.html"))
    args = ap.parse_args(argv)

    try:
        slides = compile_slides(load_frontmatter(args.design), parse_deck(args.deck))
    except Exception as e:
        print("PREFLIGHT FAIL {}".format(e))
        return 1

    css = THEME_CSS.read_text(encoding="utf-8")
    Path(args.out_md).write_text(render_markdown(slides, css), encoding="utf-8")

    marp = shutil.which("marp")
    if not marp:
        print("FAIL marp CLI not found on PATH (install: npm i -g @marp-team/marp-cli)")
        return 1
    proc = subprocess.run([marp, args.out_md, "-o", args.out_html],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print("FAIL marp render ({}): {}".format(proc.returncode, proc.stderr.strip()))
        return 1
    print("Build OK: {} ({} slides) -> {}".format(
        args.out_md, len(slides), args.out_html))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
