"""Data-driven PPTX renderers.

Each archetype renderer is a pure function: ``(ctx, slide, geometry, args)``.
Geometry comes from ``registry.json``; all deck text from ``slides_data``.
Creation order within each renderer is preserved exactly to keep output
content-level deterministic vs the V1.0 engine.
"""

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

from .core import Ctx


def _align(name):
    return {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER}.get(name, PP_ALIGN.LEFT)


def _anchor(name):
    return {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE}.get(name, MSO_ANCHOR.TOP)


def render_hero_center(ctx, slide, geom, args):
    ctx.fill_rect(slide, geom["banner_rect"]["box"], geom["banner_rect"]["fill"])
    k = geom["kicker"]
    ctx.add_text(slide, k["box"], args["kicker"], k["size"], k["color"], bold=k["bold"])
    t = geom["title_box"]
    ctx.add_text(slide, t["box"], args["title"], t["size"], t["color"], bold=t["bold"],
                 align=_align(t["align"]), anchor=_anchor(t["anchor"]))
    s = geom["subtitle_box"]
    ctx.add_text(slide, s["box"], args["subtitle"], s["size"], s["color"],
                 align=_align(s["align"]))
    tk = geom["takeaway_box"]
    ctx.add_text(slide, tk["box"], args["takeaway"], tk["size"], tk["color"],
                 align=_align(tk["align"]))
    ctx.fill_rect(slide, geom["divider_rect"]["box"], geom["divider_rect"]["fill"])
    m = geom["meta_box"]
    ctx.add_text(slide, m["box"], args["meta"], m["size"], m["color"], align=_align(m["align"]))


def render_split_50_50(ctx, slide, geom, args):
    ctx.slide_header(slide, args["title"])
    ctx.fill_rect(slide, geom["left_rect"]["box"], geom["left_rect"]["fill"])
    la = geom["left_anchor_box"]
    ctx.add_text(slide, la["box"], args["left_anchor"], la["size"], la["color"],
                 bold=la["bold"], anchor=_anchor(la["anchor"]),
                 line_spacing=la["line_spacing"])
    ctx.add_bullets(slide, geom["right_bullets_box"]["box"], args["right_bullets"])
    ctx.accent_strip(slide)


def render_metric_hero_row(ctx, slide, geom, args):
    ctx.slide_header(slide, args["title"])
    card_rect = geom["card_rect"]
    for left, metric in zip(geom["card_lefts"], args["metrics"]):
        ctx.fill_rect(slide, [left, card_rect["top"], card_rect["dims"][0], card_rect["dims"][1]],
                      card_rect["fill"])
        n = geom["number_box"]
        ctx.add_text(slide, [left + n["offset"][0], n["offset"][1],
                             n["size_dims"][0], n["size_dims"][1]],
                     metric["number"], n["size"], n["color"], bold=n["bold"],
                     anchor=_anchor(n["anchor"]))
        lab = geom["label_box"]
        ctx.add_text(slide, [left + lab["offset"][0], lab["offset"][1],
                             lab["size_dims"][0], lab["size_dims"][1]],
                     metric["label"], lab["size"], lab["color"], bold=lab["bold"])
        c = geom["context_box"]
        ctx.add_text(slide, [left + c["offset"][0], c["offset"][1],
                             c["size_dims"][0], c["size_dims"][1]],
                     metric["context"], c["size"], c["color"], line_spacing=c["line_spacing"])
    ctx.accent_strip(slide)


def render_card_row_3(ctx, slide, geom, args):
    ctx.slide_header(slide, args["title"])
    card = geom["cards"]
    card_rect = card["card_rect"]
    strip = card["top_strip"]
    for left, card_args, strip_color in zip(geom["card_lefts"], args["cards"], strip["colors"]):
        ctx.fill_rect(slide, [left, card_rect["top"],
                              card_rect["dims"][0], card_rect["dims"][1]], card_rect["fill"])
        if strip_color:
            ctx.fill_rect(slide, [left, card_rect["top"],
                                  card_rect["dims"][0], strip["height"]], strip_color)
        h = card["header_box"]
        ctx.add_text(slide, [left + h["offset"][0], h["offset"][1],
                             h["size_dims"][0], h["size_dims"][1]],
                     card_args["header"], h["size"], h["color"], bold=h["bold"])
        b = card["bullets_box"]
        ctx.add_bullets(slide, [left + b["offset"][0], b["offset"][1],
                                b["size_dims"][0], b["size_dims"][1]],
                        card_args["bullets"], size=b["size"], bold_lead=b["bold_lead"])
    ctx.accent_strip(slide)


def render_grid_2x2(ctx, slide, geom, args):
    ctx.slide_header(slide, args["title"])
    quad_rect = geom["quad_rect"]
    title = geom["title_box"]
    bullets = geom["bullets_box"]
    for pos, quad in zip(geom["quad_positions"], args["quadrants"]):
        ctx.fill_rect(slide, [pos["left"], pos["top"],
                              quad_rect["dims"][0], quad_rect["dims"][1]], quad_rect["fill"])
        ctx.add_text(slide, [pos["left"] + title["offset"][0], pos["top"] + title["offset"][1],
                             title["size_dims"][0], title["size_dims"][1]],
                     quad["title"], title["size"], pos["header_color"], bold=title["bold"])
        ctx.add_bullets(slide, [pos["left"] + bullets["offset"][0], pos["top"] + bullets["offset"][1],
                                bullets["size_dims"][0], bullets["size_dims"][1]],
                        quad["bullets"], size=bullets["size"], bold_lead=bullets["bold_lead"],
                        line_spacing=bullets["line_spacing"])
    ctx.accent_strip(slide)


def render_process_timeline(ctx, slide, geom, args):
    ctx.slide_header(slide, args["title"])
    n = len(args["steps"])
    gap = geom["gap"]
    node_w = (geom["track_width"] - (n - 1) * gap) / n
    positions = [geom["start_left"] + i * (node_w + gap) for i in range(n)]
    card_rect = geom["card_rect"]
    header = geom["header_box"]
    summary = geom["summary_box"]
    for left, step in zip(positions, args["steps"]):
        ctx.fill_rect(slide, [left, card_rect["top"], node_w, card_rect["height"]],
                      card_rect["fill"])
        ctx.add_text(slide, [left + header["x_off"], header["y"],
                             node_w - 2 * header["x_off"], header["height"]],
                     step["header"], header["size"], header["color"], bold=header["bold"])
        ctx.add_text(slide, [left + summary["x_off"], summary["y"],
                             node_w - 2 * summary["x_off"], summary["height"]],
                     step["summary"], summary["size"], summary["color"])
    ctx.accent_strip(slide)


_RENDERERS = {
    "HERO_CENTER": render_hero_center,
    "SPLIT_50_50": render_split_50_50,
    "METRIC_HERO_ROW": render_metric_hero_row,
    "CARD_ROW_3": render_card_row_3,
    "GRID_2X2": render_grid_2x2,
    "PROCESS_TIMELINE": render_process_timeline,
}


def build_pptx(slides_data, registry, out_path, total_slides=None):
    """Render a presentation from ``slides_data`` against ``registry``.

    Deterministic at content level: same inputs produce byte-identical XML
    parts (zip entry metadata from python-pptx may still vary).
    """
    prs = Presentation()
    canvas = registry["meta"]["canvas"]
    prs.slide_width = Inches(canvas["width"])
    prs.slide_height = Inches(canvas["height"])
    blank = prs.slide_layouts[6]
    ctx = Ctx(registry)

    for data in slides_data:
        slide = prs.slides.add_slide(blank)
        archetype = registry["archetypes"][data["type"]]
        renderer = _RENDERERS[data["type"]]
        renderer(ctx, slide, archetype["geometry"], data["args"])
        ctx.set_notes(slide, data["voiceover"], data["mindset"])

    prs.save(str(out_path))
    expected = total_slides if total_slides is not None else len(slides_data)
    actual = len(prs.slides._sldIdLst)
    assert actual == expected, "Expected {}, got {}".format(expected, actual)
    print("Build OK: {} with {} slides".format(out_path, actual))
    return out_path