"""Compile design.md frontmatter + parsed deck-content into engine slides (B3b).

Single-source chain (A1/A3): deck-content.md is the only copy source. The
compiler asserts the three-source gate (deck frontmatter == design
frontmatter == parsed slides, and per-slide layout == design
``slide_archetypes``), injects ``action_title`` as engine ``args.title``,
and strips trailing newlines from block scalars so hand-authored ``|`` and
``|-`` voiceovers compile identically.
"""

from .validate_design import load_frontmatter  # noqa: F401  (re-exported convenience)

__all__ = ["CompileError", "compile_slides", "load_frontmatter"]


class CompileError(Exception):
    """Raised on any three-source inconsistency during compilation."""


def compile_slides(design_fm, deck):
    """Return the engine slides list (shape of slides_data.json entries)."""
    n_deck = deck["frontmatter"]["total_slides"]
    n_design = design_fm["total_slides"]
    if not (n_deck == n_design == len(deck["slides"])):
        raise CompileError(
            "three-source slide count mismatch: deck frontmatter={} "
            "design={} parsed={}".format(n_deck, n_design, len(deck["slides"])))
    mapping = {str(k): v for k, v in design_fm["slide_archetypes"].items()}

    slides = []
    for i, slide in enumerate(deck["slides"], 1):
        mapped = mapping.get(str(i))
        if mapped != slide["layout"]:
            raise CompileError(
                "slide {}: design.slide_archetypes says {} but deck layout "
                "is {}".format(i, mapped, slide["layout"]))
        args = {"title": slide["action_title"]}
        args.update(slide["args"])
        slides.append({
            "type": slide["layout"],
            "args": args,
            "voiceover": slide["voiceover"].rstrip("\n"),
            "mindset": slide["mindset"],
        })
    return slides
