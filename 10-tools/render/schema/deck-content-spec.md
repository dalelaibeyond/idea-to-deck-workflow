# deck-content.md Machine Contract — A4 Spec v1

> **Authority:** this document defines the parseable contract of `06-outputs/deck-content.md`.
> **Consumers:** `10-tools/render/parse_deck.py` (parser), `10-tools/render/compile.py` (B3b compiler), C2 post-build checks.
> **Design rulings:** format designed from best practices, independent of any legacy corpus (review-11th 决策1); output language defaults to English unless explicitly specified (review-11th 决策2).

---

## 1. Design principles

1. **Unambiguous delimiting.** Every machine-read field lives inside a fenced YAML block. Free prose never carries machine data, so CJK quotes `「」`, English quotes, colons, em-dashes, and newlines inside field values can never break parsing.
2. **Single source per fact.** The action title exists once (slide-level `action_title`); the compiler injects it into engine `args.title`. Slide headings carry no title text, so nothing can drift.
3. **Schema-enforced shape.** Each archetype's `args` has a closed schema (`deck-content.schema.json`): exact keys, exact cardinalities (3 metrics, 3 cards, 4 quadrants, 3–5 steps). Structural errors fail before rendering.
4. **Human review stays first-class.** The file remains valid Markdown: headings navigate, fenced blocks render as highlighted YAML on GitHub (info string `yaml slide` — first token drives highlighting).

## 2. File structure

```
---                                   ← file frontmatter (YAML, required)
total_slides: 6
audience: "..."
core_objective: "..."
scenario: "..."                       ← optional
language: en-US                       ← optional; DEFAULT "en-US" when absent
---

## Slide 1                            ← exact form; sequential 1..N; no title text

```yaml slide                          ← fence info string MUST be exactly "yaml slide"
layout: HERO_CENTER                   ← archetype name (design.md layout_tag_vocab)
action_title: "..."
args:                                 ← per-archetype schema (§4); NO title key here
  kicker: "..."
  ...
voiceover: |                          ← ALWAYS a literal block scalar (multi-line safe)
  Full script. Any quotes ： colons
  「」—— dashes and line breaks allowed.
mindset: "..."
```                                    ← exactly one fence per slide section

## Slide 2
...
```

## 3. Rules (all mechanically validated)

| # | Rule | Failure mode |
|:-|:--|:--|
| R1 | File starts with `---` frontmatter; keys `total_slides`/`audience`/`core_objective` required; `scenario`/`language` optional; no other keys | `frontmatter` error |
| R2 | `language` absent ⇒ parser applies default `en-US`; otherwise any BCP-47-style tag passes through | — |
| R3 | Body contains exactly the headings `## Slide 1` … `## Slide N` (exact text, sequential, N == `total_slides`); nothing else at heading level | `structure` error |
| R4 | Each slide section contains **exactly one** fenced block with info string `yaml slide`; no other fences in the file | `structure` error |
| R5 | Slide block keys are exactly `layout`, `action_title`, `args`, `voiceover`, `mindset` (closed set) | schema error |
| R6 | `layout` ∈ archetype vocabulary (schema enum; compile step additionally asserts equality with `design.md` `slide_archetypes`) | schema / compile error |
| R7 | `args` matches the per-archetype schema (§4) — closed keys, non-empty strings, exact cardinalities | schema error |
| R8 | `voiceover` authored as block scalar `|`; parsed value non-empty. `mindset` non-empty | schema error |
| R9 | Bullet strings may use a single `Lead: body` prefix consumed by the renderer; everything after the first colon is body | renderer behavior |

## 4. Per-archetype `args` schemas

All string fields non-empty. `title` is absent everywhere — injected from `action_title` by the compiler.

| Archetype | Keys (all required) | Cardinality |
|:--|:--|:--|
| `HERO_CENTER` | `kicker`, `subtitle`, `takeaway`, `meta` | — |
| `SPLIT_50_50` | `left_anchor`, `right_bullets[]` | ≥ 1 bullet |
| `METRIC_HERO_ROW` | `metrics[] {number, label, context}` | exactly 3 |
| `CARD_ROW_3` | `cards[] {header, bullets[]}` | exactly 3 cards, ≥ 1 bullet each |
| `GRID_2X2` | `quadrants[] {title, bullets[]}` | exactly 4 quadrants, ≥ 1 bullet each |
| `PROCESS_TIMELINE` | `steps[] {header, summary}` | 3–5 steps |

## 5. Parser contract

`parse_deck(path)` → `{"frontmatter": {...}, "slides": [{layout, action_title, args, voiceover, mindset}, ...]}`.

1. Extract frontmatter with `^---\n(.*?)\n---\n` (file must start with it).
2. Split body on `^## Slide (\d+)$`; assert the heading sequence is exactly `1..N`.
3. Per section, extract the unique ` ```yaml slide ` fence; `yaml.safe_load`; validate against `deck-content.schema.json` (`slide` definition).
4. Apply R2 default. Slide count must equal `total_slides`.

Exit/exception contract: any violation raises `DeckError` with a message prefixed by the failing unit (`frontmatter:` / `slide N:` / `structure:`) — usable as a Phase 5 preflight gate (fail-fast, no partial output).

## 6. Relationship to other sources

- `design.md` frontmatter (`layout_tag_vocab`, `slide_archetypes`, `total_slides`) must agree with this file — asserted by the compiler (A3 derivation, C1 preflight).
- Engine geometry stays in `registry.json` (P9 ruling, review-10th); this file carries content only.
- `slides_data.json` becomes a compiler-emitted debug artifact once B3b lands; it is no longer hand-maintained.
