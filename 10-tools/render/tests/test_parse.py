#!/usr/bin/env python3
"""Fixture acceptance for parse_deck (A4) — positive and negative cases.

Usage:
    python test_parse.py

Positive: deck-en.md (6 slides, one per archetype, language defaults to
en-US), deck-zh.md (zh-CN, CJK stress: 「」quotes, full-width colons,
em-dashes, multi-line voiceovers).
Negative: three bad fixtures must each fail with the expected unit prefix.
"""

import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
TOOLS = HERE.parent.parent
sys.path.insert(0, str(TOOLS))

from render.parse_deck import DeckError, parse_deck  # noqa: E402

FIX = HERE / "fixtures"
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def _raw_frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    return yaml.safe_load(FRONTMATTER_RE.match(text).group(1))


def expect_ok(name, slide_count, language):
    parsed = parse_deck(FIX / name)
    assert len(parsed["slides"]) == slide_count, \
        "{}: expected {} slides, got {}".format(name, slide_count, len(parsed["slides"]))
    assert parsed["frontmatter"]["language"] == language, \
        "{}: expected language {}, got {}".format(name, language,
                                                  parsed["frontmatter"]["language"])
    print("PASS ok        {} ({} slides, language={})".format(
        name, slide_count, language))


def expect_fail(name, unit_prefix, contains):
    try:
        parse_deck(FIX / name)
    except DeckError as e:
        msg = str(e)
        assert msg.startswith(unit_prefix), \
            "{}: expected prefix {!r}, got {!r}".format(name, unit_prefix, msg)
        assert contains in msg, \
            "{}: expected {!r} in {!r}".format(name, contains, msg)
        print("PASS fail      {} -> {}".format(name, msg.splitlines()[0][:100]))
        return
    raise AssertionError("{}: expected DeckError, parsed successfully".format(name))


def main():
    expect_ok("deck-en.md", 6, "en-US")
    expect_ok("deck-zh.md", 3, "zh-CN")

    # language default: deck-en.md omits the field, parser must apply en-US
    assert "language" not in _raw_frontmatter(FIX / "deck-en.md"), \
        "deck-en.md should omit language to exercise the default"
    layouts = [s["layout"] for s in parse_deck(FIX / "deck-en.md")["slides"]]
    assert set(layouts) == {"HERO_CENTER", "SPLIT_50_50", "METRIC_HERO_ROW",
                            "CARD_ROW_3", "GRID_2X2", "PROCESS_TIMELINE"}, \
        "deck-en.md must cover all 6 archetypes exactly once, got {}".format(layouts)

    # CJK stress: multi-line voiceover with 「」、：、—— round-trips verbatim
    zh = parse_deck(FIX / "deck-zh.md")
    v1 = zh["slides"][0]["voiceover"]
    assert "\n" in v1 and "「全检」" in v1 and "——" in v1, \
        "deck-zh.md voiceover must preserve newlines and CJK punctuation"
    assert "：" in zh["slides"][1]["args"]["right_bullets"][0], \
        "deck-zh.md bullets must preserve full-width colons"

    expect_fail("deck-bad-structure.md", "structure:", "!= expected sequential")
    expect_fail("deck-bad-vocab.md", "slide 1:", "TIMELINE_PROCESS")
    expect_fail("deck-bad-args.md", "slide 1:", "quadrants")

    print("ALL FIXTURE CASES PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
