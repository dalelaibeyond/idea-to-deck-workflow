---
total_slides: 6
theme_name: "Enterprise Strategic Navy + Teal Accent"
aspect_ratio: "16:9 (13.333 x 7.500 in)"
canvas_background: "#FFFFFF"
primary_brand: "#0F172A"
secondary_brand: "#2563EB"
accent_metric: "#0D9488"
surface_card: "#F8FAFC"
text_primary: "#1E293B"
text_muted: "#64748B"
font_family_header: "Segoe UI, Microsoft YaHei, sans-serif"
font_family_body: "Segoe UI, PingFang SC, sans-serif"
---

# Global Layout Guidelines
* Canvas Dimensions: 13.333 in width x 7.500 in height.
* Global Header: Action Title at Top=0.8 in, Left=0.8 in, Width=11.7 in, Height=0.9 in, Font=24pt Bold.
* Type Scale: Action Title 24pt Bold | Card Header 16pt Bold | Body Bullets 12-14pt | Hero Metric 42pt Bold.
* Designated Exception: `HERO_CENTER` (cover slide) overrides the Action Title to 36pt Bold and the Subtitle to 18pt — this exception is defined in the Archetype Registry below and applies ONLY to `HERO_CENTER`.
* Accent bar: A 0.12 in tall `accent_metric` strip across the bottom of every content slide (not the cover) for visual consistency.

# Archetype Registry (Geometric & CSS Specifications)

### `HERO_CENTER`
* **Python-pptx:** Title (Left=1.5", Top=2.6", Width=10.3", Height=1.8", 36pt Bold); Subtitle (Left=1.5", Top=4.6", Width=10.3", Height=1.0", 18pt). Lead takeaway (Left=1.5", Top=5.7", Width=10.3", Height=0.9", 14pt, `text_muted`). Metadata (Left=1.5", Top=6.7", Width=10.3", Height=0.5", 11pt, `text_muted`).
* **Marp CSS:** `display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; height: 80%;`

### `SPLIT_50_50`
* **Python-pptx:** Left Container (Left=0.8", Top=2.0", Width=5.5", Height=4.6", 20pt Bold, left-aligned, `primary_brand`); Right Container (Left=6.8", Top=2.0", Width=5.7", Height=4.6", 13pt Bullets, `text_primary`). Left anchor accented with `accent_metric` key number highlight.
* **Marp CSS:** `display: grid; grid-template-columns: 1fr 1fr; gap: 32px; margin-top: 24px;`

### `CARD_ROW_3`
* **Python-pptx:** 3 Cards at Top=2.0", Height=4.6", Width=3.6", Gap=0.4". Left positions: Card 1=0.8", Card 2=4.8", Card 3=8.8". Header 16pt Bold, Bullets 12pt. Card 2 accented with `secondary_brand` top border strip.
* **Marp CSS:** `display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 24px;`

### `GRID_2X2`
* **Python-pptx:** 4 Quadrants. Row 1 Top=1.9", Row 2 Top=4.3", Height=2.3". Col 1 Left=0.8", Col 2 Left=6.8", Width=5.6". Header 15pt Bold, Bullets 12pt. Quadrant 4 (Enablement) rendered with `accent_metric` header color to signal activation.
* **Marp CSS:** `display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr; gap: 20px; margin-top: 20px;`

### `METRIC_HERO_ROW`
* **Python-pptx:** 3 Stat Cards. Top=2.2", Height=4.2", Width=3.6", Gap=0.4". Left positions: Card 1=0.8", Card 2=4.8", Card 3=8.8". Big Metric Box (Height=1.8", 42pt Bold, `accent_metric`), Label Box (Height=2.2", 14pt Bold, `primary_brand`), Context line 11pt `text_muted`.
* **Marp CSS:** `display: flex; justify-content: space-around; align-items: stretch; gap: 24px; margin-top: 32px;`

### `PROCESS_TIMELINE`
* **Python-pptx:** 3-5 Sequence Nodes at Top=2.8", Height=3.5", Gap=0.4". Adaptive Node Width = (11.73 - (N-1)*0.4) / N (N=3: Width=3.64", N=4: Width=2.63", N=5: Width=2.03"). Step Header 14pt Bold, Summary 11pt.
* **Marp CSS:** `display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-top: 40px;`

# Slide-to-Archetype Mapping

## Slide 1: ICS's Hardware-Driven Model Faces Structural Margin Compression
* Archetype: `HERO_CENTER`
* Palette Focus: `primary_brand` for Title, `text_muted` for Subtitle and Metadata.

## Slide 2: Legacy Hardware Resale No Longer Sustains Profitable Growth
* Archetype: `SPLIT_50_50`
* Palette Focus: Left anchor `accent_metric` (highlight "84%"), Right bullets `text_primary`. Bottom accent strip.

## Slide 3: AI Agents Will Create a $52B Market by 2030 — and the Philippines Is Wide Open
* Archetype: `METRIC_HERO_ROW`
* Palette Focus: Metric numbers `accent_metric`, labels `primary_brand`. Card 3 context line highlighted to emphasize "2%".

## Slide 4: ICS's 40 Years of Customer Trust Is the Unfair Advantage in AI Delivery
* Archetype: `CARD_ROW_3`
* Palette Focus: Card 2 (Domain Expertise) accented with `secondary_brand` top border strip.

## Slide 5: A Focused Three-Pillar Roadmap Transforms ICS from Hardware Reseller to AI SI
* Archetype: `GRID_2X2`
* Palette Focus: Quadrant 4 (Enablement Engine) header in `accent_metric` to signal activation.

## Slide 6: Board Approval of AI Agent Investment Secures ICS's Next Decade
* Archetype: `SPLIT_50_50`
* Palette Focus: Left anchor "Approve the AI Agent Practice" in `accent_metric`, right bullets `text_primary`. Bottom accent strip signals call-to-action.