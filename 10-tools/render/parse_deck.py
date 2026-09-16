#!/usr/bin/env python3
"""Parse and validate deck-content.md against the A4 spec v1.

Usage:
    python parse_deck.py 06-outputs/deck-content.md [--emit-json out.json]

Contract: ``10-tools/render/schema/deck-content-spec.md``. Every machine
field lives inside a fenced ``yaml slide`` block; free prose never carries
machine data, so CJK quotes, colons, dashes and newlines inside values are
inherently safe. Language defaults to en-US when the frontmatter omits it
(review-11th ruling 2).

Exit 0 == parsed and valid, 1 == first violation (fail-fast preflight).
"""

import argparse
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema" / "deck-content.schema.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HEADING_RE = re.compile(r"^## Slide (\d+)\s*$", re.M)
FENCE_RE = re.compile(r"^```yaml slide\s*\n(.*?)^```\s*$", re.S | re.M)

DEFAULT_LANGUAGE = "en-US"


class DeckError(Exception):
    """Raised on any A4 contract violation; message is prefixed by unit."""


def _slide_schema(schema_doc):
    return {"$ref": "#/definitions/slide", "definitions": schema_doc["definitions"]}


def _fm_schema(schema_doc):
    return {"$ref": "#/definitions/frontmatter", "definitions": schema_doc["definitions"]}


def _validate(instance, subschema, unit):
    try:
        jsonschema.validate(instance=instance, schema=subschema)
    except jsonschema.ValidationError as e:
        raise DeckError("{}: {}: {}".format(unit, e.json_path, e.message))


def parse_deck(path, schema_doc=None):
    """Parse deck-content.md -> {"frontmatter": {...}, "slides": [...]}."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    schema_doc = schema_doc or json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    m = FRONTMATTER_RE.match(text)
    if not m:
        raise DeckError("frontmatter: file must start with a '---' YAML block")
    try:
        fm = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        raise DeckError("frontmatter: invalid YAML ({})".format(e))
    if not isinstance(fm, dict):
        raise DeckError("frontmatter: not a mapping")
    _validate(fm, _fm_schema(schema_doc), "frontmatter")
    fm.setdefault("language", DEFAULT_LANGUAGE)

    body = text[m.end():]
    headings = list(HEADING_RE.finditer(body))
    expected = list(range(1, fm["total_slides"] + 1))
    got = [int(h.group(1)) for h in headings]
    if got != expected:
        raise DeckError("structure: slide headings {} != expected sequential {}".format(
            got, expected))

    slides = []
    for i, h in enumerate(headings):
        unit = "slide {}".format(h.group(1))
        section_end = headings[i + 1].start() if i + 1 < len(headings) else len(body)
        section = body[h.end():section_end]
        fences = FENCE_RE.findall(section)
        if len(fences) != 1:
            raise DeckError("{} expected exactly one 'yaml slide' fence, found {}".format(
                unit, len(fences)))
        try:
            block = yaml.safe_load(fences[0])
        except yaml.YAMLError as e:
            raise DeckError("{} invalid YAML ({})".format(unit, e))
        if not isinstance(block, dict):
            raise DeckError("{} block is not a mapping".format(unit))
        _validate(block, _slide_schema(schema_doc), unit)
        slides.append(block)

    return {"frontmatter": fm, "slides": slides}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("deck_path", help="path to deck-content.md")
    ap.add_argument("--emit-json", help="write parsed structure to this JSON file")
    args = ap.parse_args(argv)

    try:
        parsed = parse_deck(args.deck_path)
    except DeckError as e:
        print("PARSE FAIL {}".format(e))
        return 1

    if args.emit_json:
        Path(args.emit_json).write_text(
            json.dumps(parsed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    layouts = [s["layout"] for s in parsed["slides"]]
    print("PARSE OK   {} slides [{}] language={}".format(
        len(parsed["slides"]), ", ".join(layouts),
        parsed["frontmatter"]["language"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
