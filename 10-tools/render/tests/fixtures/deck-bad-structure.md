---
total_slides: 2
audience: "negative fixture"
core_objective: "must fail: slide 2 heading missing (non-sequential)"
---

## Slide 1

```yaml slide
layout: HERO_CENTER
action_title: "Structure fixture"
args:
  kicker: "k"
  subtitle: "s"
  takeaway: "t"
  meta: "m"
voiceover: |
  valid block
mindset: "valid"
```

## Slide 3

```yaml slide
layout: SPLIT_50_50
action_title: "Skipped slide 2"
args:
  left_anchor: "anchor"
  right_bullets:
    - "bullet"
voiceover: |
  valid block
mindset: "valid"
```
