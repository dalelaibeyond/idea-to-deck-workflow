# Advice for Visual Design v1.0

## Core recommendation

`design.md` should be allowed to fully exercise the model's design judgment, but it must remain structured in two layers:

1. Human-readable design intelligence layer
2. Machine-readable execution layer

This separation ensures that the Agent can act like a senior design expert while the pipeline still remains stable, testable, and exportable.

---

## Why this is needed

The current design artifact can easily drift into one of two bad extremes:

- Too mechanical: the model only copies a template and never reasons about visual hierarchy.
- Too freeform: the model writes poetic design commentary but the renderer cannot consume it reliably.

Neither is ideal.

The right pattern is:

- The Agent thinks like a professional designer.
- The machine consumes a structured, structured, verifiable specification.

---

## Recommended design structure

### A. Human-readable design intelligence layer

This section should be written for humans and strong design-oriented Agents.

It should include:

- design intent
- audience-fit logic
- visual hierarchy decisions
- information density management
- emphasis strategy
- palette rationale
- typography rationale
- layout rationale
- slide-level design thinking
- brand / message alignment

This is where the Agent can demonstrate deep design capability.

Examples of content here:

- Why this page should feel decisive and minimal
- Why the left/right split is better than a 3-card layout
- Why the accent color is used on metrics only and not every block
- Why the page should prioritize comparison over narrative
- Why a subdued palette supports the executive audience better than a lively one

This layer is not meant to be machine-executed. It is meant to be human-credible and design-credible.

---

### B. Machine-readable execution layer

This section should be strict and structured.

It should include:

- theme tokens
- color hex values
- typography scale
- layout tag vocabulary
- archetype registry
- width / height / offset values
- slide-to-archetype mapping
- validation-friendly metadata

This layer is what the renderer and schema validator read.

This is the part that must stay stable, deterministic, and parsable.

---

## Design skill integration

The Agent should be allowed to absorb strong visual-design ideas from advanced GitHub skill patterns, but those ideas should be translated into disciplined design principles rather than left as vague instructions.

Examples of useful design principles:

- hierarchy before decoration
- emphasis through contrast, not clutter
- use accent strategically instead of everywhere
- support information scanning, not just narrative flow
- match visual energy to audience and scenario
- keep emotional tone consistent across the deck
- reduce unnecessary visual noise

These should be treated as professional design principles, then converted into actionable design constraints in the machine-readable layer.

---

## Practical rule

A good rule for the design artifact is:

- The design expert can reason freely in the human-readable section.
- The pipeline must only consume the machine-readable section for execution and validation.

This preserves both creative quality and engineering stability.

---

## Recommended output pattern

The `design.md` file should be organized like this:

```markdown
---
# machine readable frontmatter
---

# Design Intent
[human reading / reasoning layer]

# Visual System
[palette, typography, tone, rationale]

# Archetype Registry
[human explanation + machine spec]

# Slide-to-Archetype Mapping
[structured mapping]
```

This gives the Agent room to think, while also making the file usable by automation.

---

## Key caution

Do not let the design file become a “free-form design essay” with no executable contract.

Do not let the rendering layer become a black box where the Agent merely interprets the design in a different language every time.

The goal is not to reduce the Agent's intelligence. The goal is to convert intelligence into disciplined, consistent design output.

---

## Bottom line

Yes — `design.md` should give the Agent room to behave like a top-tier design expert.

But the artifact should intentionally separate:

- design thinking: rich, nuanced, human-readable
- design execution: strict, schema-friendly, machine-usable

This is the cleanest way to combine expert design judgment with a stable rendering pipeline.
