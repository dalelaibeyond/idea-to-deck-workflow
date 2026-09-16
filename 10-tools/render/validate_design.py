#!/usr/bin/env python3
"""S2 pre-flight: validate design.md frontmatter (A2) + engine cross-checks.

Usage:
    python validate_design.py 06-outputs/design.md

Checks:
1. YAML frontmatter validates against ``schema/design.schema.json``.
2. ``layout_tag_vocab`` == ``registry.json`` archetype keys (exact set).
3. ``slide_archetypes`` maps every slide (1..total_slides) to a vocab member.
4. Theme hex values match ``registry.json`` theme (single-source) and every
   geometry color reference resolves to a defined theme key or raw hex.
5. ``fonts.pptx`` == ``registry.json`` fonts (html fonts defer to S3/B4).
6. ``type_scale`` named sizes match the geometry register (engine truth).
7. ``registry.archetypes`` keys == ``pptx_engine._RENDERERS`` keys, and each
   ``render_fn`` equals its engine entry exactly (no substring pass).

Exit 0 == all pass, 1 == first failure (deterministic, pre-check gate).
"""

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema" / "design.schema.json"
REGISTRY_PATH_DEFAULT = HERE / "registry.json"
ENGINE_PATH = HERE / "pptx_engine.py"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

BAR = 60 * "-"


def load_frontmatter(design_path):
    text = Path(design_path).read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise SystemExit("no YAML frontmatter found in %s" % design_path)
    data = yaml.safe_load(m.group(1))
    if not isinstance(data, dict):
        raise SystemExit("frontmatter is not a mapping in %s" % design_path)
    return data


def check_schema(data, schema):
    jsonschema.validate(instance=data, schema=schema)
    return "frontmatter matches design.schema.json"


def check_vocab(data, registry):
    vocab = set(data["layout_tag_vocab"])
    keys = set(registry["archetypes"])
    missing = vocab - keys
    extra = keys - vocab
    assert not missing and not extra, \
        "vocab ≠ registry: missing={} extra={}".format(sorted(missing), sorted(extra))
    return "layout_tag_vocab == registry archetypes ({} tags)".format(len(vocab))


def check_slide_map(data):
    n = data["total_slides"]
    vocab = set(data["layout_tag_vocab"])
    mapping = {str(k): v for k, v in data["slide_archetypes"].items()}
    expected_keys = set(str(i) for i in range(1, n + 1))
    got_keys = set(mapping)
    assert got_keys == expected_keys, \
        "slide_archetypes keys {}=? expected {}".format(sorted(got_keys), sorted(expected_keys))
    bad = {k: v for k, v in mapping.items() if v not in vocab}
    assert not bad, "slide_archetypes references outside vocab: {}".format(bad)
    return "slide_archetypes: {} slides all mapped within vocab".format(n)


def _color_fields(node, prefix=""):
    """Yield ``(path, value)`` for every color-bearing field in the registry."""
    if isinstance(node, dict):
        for k, v in node.items():
            path = "{}/{}".format(prefix, k) if prefix else k
            if k == "fill" or k == "colors" or k.endswith("color"):
                yield path, v
            else:
                yield from _color_fields(v, path)
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            yield from _color_fields(v, "{}[{}]".format(prefix, i))


def check_color_refs(registry):
    theme = registry["theme"]
    fields = list(_color_fields(registry["archetypes"], "archetypes"))
    fields += list(_color_fields(registry.get("common", {}), "common"))
    bad, checked = [], 0
    for path, value in fields:
        values = value if isinstance(value, (list, tuple)) else [value]
        for v in values:
            if v is None:
                continue
            checked += 1
            if not (isinstance(v, str) and (v in theme or HEX_RE.match(v))):
                bad.append("{}={!r}".format(path, v))
    assert not bad, "unresolvable color refs: {}".format(bad)
    return "geometry color refs resolve to theme key or hex ({} checked)".format(checked)


def check_theme_consistency(data, registry):
    theme = registry["theme"]
    for key, val in theme.items():
        assert key in data and data[key] == val, \
            "theme key {} mismatches registry (design={} engine={})".format(
                key, data.get(key), val)
    for key in ("canvas_background", "primary_brand", "secondary_brand",
                "accent_metric", "surface_card", "text_primary", "text_muted"):
        assert key in theme, "engine registry missing theme key {}".format(key)
    return "theme hex == registry.theme ({} keys)".format(len(theme))


def check_type_scale(data, registry):
    expected = {
        "action_title": ["common", "slide_header", "title_box", "size"],
        "hero_cover_title": ["archetypes", "HERO_CENTER", "geometry", "title_box", "size"],
        "hero_cover_subtitle": ["archetypes", "HERO_CENTER", "geometry", "subtitle_box", "size"],
        "card_header": ["archetypes", "CARD_ROW_3", "geometry", "cards", "header_box", "size"],
        "grid_quadrant_header": ["archetypes", "GRID_2X2", "geometry", "title_box", "size"],
        "hero_metric": ["archetypes", "METRIC_HERO_ROW", "geometry", "number_box", "size"],
        "meta_text": ["archetypes", "HERO_CENTER", "geometry", "meta_box", "size"],
    }
    for name, path in expected.items():
        node = registry
        for part in path:
            node = node[part]
        assert data["type_scale"][name] == node, \
            "type_scale.{}= {} but engine {}={}".format(name, data["type_scale"][name],
                                                         "/".join(path), node)
    assert data["type_scale"]["body_bullets_min"] <= data["type_scale"]["body_bullets_max"]
    return "type_scale named sizes match engine geometry ({} refs)".format(len(expected))


def check_fonts(data, registry):
    fonts = registry.get("fonts")
    assert isinstance(fonts, dict) and fonts, "engine registry missing fonts"
    assert data["fonts"]["pptx"] == fonts, \
        "fonts.pptx {} != registry.fonts {}".format(data["fonts"]["pptx"], fonts)
    return "fonts.pptx == registry.fonts ({})".format("/".join(sorted(set(fonts.values()))))


def check_render_fn(registry):
    src = ENGINE_PATH.read_text(encoding="utf-8")
    m = re.search(r"^_RENDERERS = \{(.*?)\}", src, re.S | re.M)
    assert m, "cannot locate _RENDERERS dict in {}".format(ENGINE_PATH)
    engine_map = dict(re.findall(r"\"([A-Z0-9_]+)\":\s*(render_\w+)", m.group(1)))
    reg_names, engine_names = set(registry["archetypes"]), set(engine_map)
    assert reg_names == engine_names, \
        "archetypes != _RENDERERS keys: missing={} extra={}".format(
            sorted(engine_names - reg_names), sorted(reg_names - engine_names))
    for name, info in registry["archetypes"].items():
        assert info["render_fn"] == engine_map[name], \
            "render_fn {} != _RENDERERS[\"{}\"]={}".format(
                info["render_fn"], name, engine_map[name])
    return "render_fn == _RENDERERS exact match ({} archetypes)".format(len(reg_names))


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("design_path", help="path to design.md")
    ap.add_argument("--registry", default=str(REGISTRY_PATH_DEFAULT))
    args = ap.parse_args(argv)

    data = load_frontmatter(args.design_path)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    registry = json.loads(Path(args.registry).read_text(encoding="utf-8"))

    checks = [
        ("schema", lambda: check_schema(data, schema)),
        ("vocab", lambda: check_vocab(data, registry)),
        ("slide_map", lambda: check_slide_map(data)),
        ("theme", lambda: check_theme_consistency(data, registry)),
        ("color_refs", lambda: check_color_refs(registry)),
        ("fonts", lambda: check_fonts(data, registry)),
        ("type_scale", lambda: check_type_scale(data, registry)),
        ("render_fn", lambda: check_render_fn(registry)),
    ]
    results = []
    for name, fn in checks:
        try:
            msg = fn()
        except jsonschema.ValidationError as e:
            print(BAR)
            print("FAIL [{}] {}".format(name, e.message))
            return 1
        except AssertionError as e:
            print(BAR)
            print("FAIL [{}] {}".format(name, e))
            return 1
        except (KeyError, TypeError) as e:
            print(BAR)
            print("FAIL [{}] unexpected: {} ({})".format(name, e, type(e).__name__))
            return 1
        results.append(msg)
    print(BAR)
    for name, msg in zip((c[0] for c in checks), results):
        print("PASS [{:11}] {}".format(name, msg))
    print(BAR)
    print("design.md pre-check OK ({})".format(args.design_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))