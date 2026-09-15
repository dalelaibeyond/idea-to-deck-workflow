#!/usr/bin/env python3
"""Idea-to-Deck Phase 5A: Native python-pptx export engine."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

TOTAL_SLIDES = 6

THEME = {
    "canvas_bg": "#FFFFFF",
    "primary": "#0F172A",
    "secondary": "#2563EB",
    "accent": "#0D9488",
    "surface": "#F8FAFC",
    "text_primary": "#1E293B",
    "text_muted": "#64748B",
}

FONT_HEADER = "Calibri"
FONT_BODY = "Calibri"


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return RGBColor(*(int(hex_str[i:i + 2], 16) for i in (0, 2, 4)))


def _fill_rect(slide, left, top, width, height, color, radius=None):
    from pptx.enum.shapes import MSO_SHAPE
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    if radius is not None:
        try:
            shape.adjustments[0] = radius
        except Exception:
            pass
    shape.fill.solid()
    shape.fill.fore_color.rgb = hex_to_rgb(color)
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape


def _add_text(slide, left, top, width, height, text, size, color, bold=False,
              align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line_spacing=1.15,
              italic=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = hex_to_rgb(color)
    run.font.name = FONT_HEADER if bold else FONT_BODY
    return box


def _add_bullets(slide, left, top, width, height, items, size=13, color_key="text_primary",
                 bold_lead=True, line_spacing=1.15):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    base_color = THEME[color_key] if color_key in THEME else color_key
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.line_spacing = line_spacing
        p.space_after = Pt(6)
        lead, _, body = item.partition(":")
        if body:
            run = p.add_run()
            run.text = "\u2022  "
            run.font.size = Pt(size)
            run.font.color.rgb = hex_to_rgb(base_color)
            r = p.add_run()
            r.text = lead + ": "
            r.font.size = Pt(size)
            r.font.bold = bold_lead
            r.font.color.rgb = hex_to_rgb(base_color)
            r.font.name = FONT_BODY
            r2 = p.add_run()
            r2.text = body
            r2.font.size = Pt(size)
            r2.font.bold = False
            r2.font.color.rgb = hex_to_rgb(base_color)
            r2.font.name = FONT_BODY
        else:
            run = p.add_run()
            run.text = "\u2022  " + lead
            run.font.size = Pt(size)
            run.font.color.rgb = hex_to_rgb(base_color)
            run.font.name = FONT_BODY
    return box


def _set_notes(slide, voiceover, mindset):
    notes = slide.notes_slide.notes_text_frame
    notes.text = "[Voiceover]\n{0}\n\n[Delivery Mindset]\n{1}".format(voiceover, mindset)


def _slide_header(slide, title):
    _fill_rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.08), THEME["primary"])
    _add_text(slide, Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.9),
              title, 24, THEME["primary"], bold=True)


def _accent_strip(slide):
    _fill_rect(slide, Inches(0), Inches(7.30), Inches(13.333), Inches(0.16), THEME["accent"])


def render_hero_center(slide, title, subtitle, takeaway, meta):
    _fill_rect(slide, Inches(0), Inches(0), Inches(13.333), Inches(2.6), THEME["primary"])
    _add_text(slide, Inches(1.0), Inches(0.7), Inches(11.3), Inches(0.5), "ICS STRATEGY", 12,
              THEME["accent"], bold=True)
    _add_text(slide, Inches(1.5), Inches(2.5), Inches(10.3), Inches(1.6),
              title, 36, "#FFFFFF", bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    _add_text(slide, Inches(1.5), Inches(4.6), Inches(10.3), Inches(0.9),
              subtitle, 18, THEME["secondary"], align=PP_ALIGN.CENTER)
    _add_text(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(1.0),
              takeaway, 14, THEME["text_muted"], align=PP_ALIGN.CENTER)
    _fill_rect(slide, Inches(4.67), Inches(6.6), Inches(4.0), Inches(0.02), THEME["secondary"])
    _add_text(slide, Inches(1.5), Inches(6.7), Inches(10.3), Inches(0.5),
              meta, 11, THEME["text_muted"], align=PP_ALIGN.CENTER)


def render_split_50_50(slide, title, left_anchor, right_bullets):
    _slide_header(slide, title)
    _fill_rect(slide, Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.6), THEME["surface"])
    _add_text(slide, Inches(1.1), Inches(2.6), Inches(4.9), Inches(3.8),
              left_anchor, 20, THEME["primary"], bold=True, anchor=MSO_ANCHOR.MIDDLE,
              line_spacing=1.2)
    _add_bullets(slide, Inches(6.8), Inches(2.2), Inches(5.7), Inches(4.4), right_bullets)
    _accent_strip(slide)


def render_metric_hero_row(slide, title, metrics):
    _slide_header(slide, title)
    positions = [(0.8, 1.0), (4.8, 2.0), (8.8, 3.0)]
    for (left, _), metric in zip(positions, metrics):
        _fill_rect(slide, Inches(left), Inches(2.2), Inches(3.6), Inches(4.4), THEME["surface"])
        _add_text(slide, Inches(left + 0.2), Inches(2.5), Inches(3.2), Inches(1.8),
                  metric["number"], 40, THEME["accent"], bold=True, anchor=MSO_ANCHOR.MIDDLE)
        _add_text(slide, Inches(left + 0.2), Inches(4.4), Inches(3.2), Inches(0.8),
                  metric["label"], 15, THEME["primary"], bold=True)
        _add_text(slide, Inches(left + 0.2), Inches(5.0), Inches(3.2), Inches(1.4),
                  metric["context"], 11, THEME["text_muted"], line_spacing=1.25)
    _accent_strip(slide)


def render_card_row_3(slide, title, cards):
    _slide_header(slide, title)
    positions = [0.8, 4.8, 8.8]
    top_strip = [None, THEME["secondary"], None]
    for left, card, strip in zip(positions, cards, top_strip):
        _fill_rect(slide, Inches(left), Inches(2.0), Inches(3.6), Inches(4.7), THEME["surface"])
        if strip:
            _fill_rect(slide, Inches(left), Inches(2.0), Inches(3.6), Inches(0.1), strip)
        _add_text(slide, Inches(left + 0.2), Inches(2.3), Inches(3.2), Inches(0.7),
                  card["header"], 16, THEME["primary"], bold=True)
        _add_bullets(slide, Inches(left + 0.2), Inches(3.1), Inches(3.2), Inches(3.4),
                     card["bullets"], size=12, bold_lead=False)
    _accent_strip(slide)


def render_grid_2x2(slide, title, quadrants):
    _slide_header(slide, title)
    boxes = [
        (0.8, 1.9, THEME["primary"]),
        (6.8, 1.9, THEME["primary"]),
        (0.8, 4.3, THEME["primary"]),
        (6.8, 4.3, THEME["accent"]),
    ]
    for (left, top, header_color), quad in zip(boxes, quadrants):
        _fill_rect(slide, Inches(left), Inches(top), Inches(5.6), Inches(2.3), THEME["surface"])
        _add_text(slide, Inches(left + 0.25), Inches(top + 0.15), Inches(5.1), Inches(0.55),
                  quad["title"], 15, header_color, bold=True)
        _add_bullets(slide, Inches(left + 0.25), Inches(top + 0.75), Inches(5.1), Inches(1.45),
                     quad["bullets"], size=12, bold_lead=False, line_spacing=1.2)
    _accent_strip(slide)


def render_process_timeline(slide, title, steps):
    _slide_header(slide, title)
    n = len(steps)
    node_w = (11.73 - (n - 1) * 0.4) / n
    positions = [0.8 + i * (node_w + 0.4) for i in range(n)]
    for left, step in zip(positions, steps):
        _fill_rect(slide, Inches(left), Inches(2.8), Inches(node_w), Inches(3.5), THEME["surface"])
        _add_text(slide, Inches(left + 0.2), Inches(3.0), Inches(node_w - 0.4), Inches(0.7),
                  step["header"], 14, THEME["primary"], bold=True)
        _add_text(slide, Inches(left + 0.2), Inches(3.9), Inches(node_w - 0.4), Inches(2.2),
                  step["summary"], 12, THEME["text_primary"])
    _accent_strip(slide)


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    blank = prs.slide_layouts[6]

    slides_data = [
        {
            "type": "hero_center",
            "args": (
                "ICS's Hardware-Driven Model Faces Structural Margin Compression",
                "48 years of client trust gives ICS the edge to lead the AI Agent era.",
                "The economics of traditional system integration are permanently changing. ICS must evolve from hardware reseller to AI services partner.",
                "ICS Board Strategy Meeting  |  AI Agent Transformation Proposal  |  September 2026",
            ),
            "voiceover": "Good morning, everyone. Thank you for gathering today. For almost half a century, ICS has built its name on one thing: supporting the Philippines' most important companies with the technology they rely on. From servers and storage to SAP implementations, our name means trust. But the market is changing underneath us. The economics of the hardware business we have known are quietly eroding, year after year. Today, I want to talk about a new direction. A direction that protects everything we have built, and turns our greatest asset — our customer relationships — into the engine of our next chapter. I am going to show you why building AI Agent capabilities is the most important strategic decision ICS can make right now.",
            "mindset": "Confident, grounded opening. Establish credibility and respect for ICS's history before introducing urgency.",
        },
        {
            "type": "split_50_50",
            "args": (
                "Legacy Hardware Resale No Longer Sustains Profitable Growth",
                "84% of integrators run hardware margins at or below 30%",
                [
                    "Single-digit servers: Server and storage margins slipped into single digits in 2025.",
                    "Declining gross margin: Integrator gross margins fell from 41.9% to 38.6% in one year.",
                    "Equipment-bound revenue: 76% of installation revenue is tied to hardware, not services.",
                    "The verdict: \"Resale stopped working as a standalone business.\" — DQ Channels",
                ],
            ),
            "voiceover": "Let's be direct about the problem. The hardware business that built ICS is no longer a source of durable profit. Across the industry, 84 percent of system integrators are now running hardware margins at 30 percent or below. Servers and storage — the heart of our CORE segment — slipped to single-digit margins this year. Industry-wide gross margins dropped by roughly three points in the last twelve months alone. And here is the structural trap: 76 percent of our installation revenue is still tied to equipment, not to the services and expertise where the value now lives. Every major industry observer says the same thing. Resale, on its own, no longer works as a business model. This is not a cyclical dip. This is a permanent reset. And it affects us directly.",
            "mindset": "Gravitas and directness. Slow down on \"permanent reset.\" Let the numbers land before moving forward.",
        },
        {
            "type": "metric_hero_row",
            "args": (
                "AI Agents Will Create a $52B Market by 2030 — and the Philippines Is Wide Open",
                [
                    {"number": "$52.6B", "label": "Global AI Agents, 2030",
                     "context": "Growing from $7.8B at 46.3% CAGR. Asia Pacific leads the curve."},
                    {"number": "$3.49B", "label": "Philippine AI market, 2030",
                     "context": "Up from $772M in 2024 — a 28.6% annual growth path."},
                    {"number": "2%", "label": "PH at Integrator stage",
                     "context": "Zero firms at AI \"Leader\" stage. First-mover window is open."},
                ],
            ),
            "voiceover": "Now, the opportunity. The global market for AI Agents is expected to grow from about eight billion dollars today to more than fifty-two billion by 2030 — a growth rate of roughly 46 percent a year. And this is not a distant Western trend. The Philippine AI market alone is projected to grow from 772 million dollars to nearly three and a half billion by 2030. Meanwhile, our own clients are hungry for AI. Seven in ten enterprises across Southeast Asia see a return on generative AI within a year. Here is the most important number for ICS: only two percent of Philippine organizations have reached what experts call the 'Integrator' stage of AI maturity. Not a single one has reached 'Leader' stage. The door is wide open. Someone will walk through it. It should be us.",
            "mindset": "Energy rises. Momentum builds through the three numbers. Emphasize \"It should be us\" with conviction.",
        },
        {
            "type": "card_row_3",
            "args": (
                "ICS's 40 Years of Customer Trust Is the Unfair Advantage in AI Delivery",
                [
                    {"header": "40 Years of Trust", "bullets": [
                        "Deep relationships with the Philippines' top 1,000 enterprises.",
                        "A 3-5 year window before AI-native entrants can match this.",
                    ]},
                    {"header": "Domain Expertise", "bullets": [
                        "IT Audit, SAP, and MDR are ready-made AI use cases.",
                        "Agentic AI delivers 30-40% productivity gains in these areas.",
                    ]},
                    {"header": "Platform Ecosystem", "bullets": [
                        "Microsoft Copilot Studio: 230,000+ organizations building agents.",
                        "Salesforce Agentforce agents grew 119% in H1 2025. They need local SIs to deploy.",
                    ]},
                ],
            ),
            "voiceover": "Why ICS? Because we are not starting from zero. First, trust. Forty-eight years of working inside the Philippines' most important companies — handling their audits, their SAP systems, their security. There is no substitute for that foundation, and no newcomer can buy it overnight. We estimate it protects our position for three to five years. Second, expertise. The work we already do — IT System Audit, SAP, and Managed Detection and Response — are exactly the use cases where AI Agents deliver thirty to forty percent productivity improvements. We do not need to invent new business; we need to make our existing business smarter. Third, the platforms have matured. Microsoft and Salesforce have built the agent engines, and they need local integrators like ICS to deploy, customize, and run them.",
            "mindset": "Confident, assured. Slow pace. Claim the advantage without arrogance — grounded in facts.",
        },
        {
            "type": "grid_2x2",
            "args": (
                "A Focused Three-Pillar Roadmap Transforms ICS from Hardware Reseller to AI SI",
                [
                    {"title": "IT Audit Automation", "bullets": [
                        "Automate compliance checks and audit report generation.",
                        "Turn labor-heavy service into scalable, high-margin revenue.",
                        "Quick win: existing audit clients, existing tools.",
                    ]},
                    {"title": "SAP Enhancement", "bullets": [
                        "Add AI monitoring and anomaly detection to SAP installs.",
                        "Upsell intelligent operations inside an existing customer base.",
                        "Quick win: 100+ SAP customers already trust ICS.",
                    ]},
                    {"title": "AI-Powered MDR", "bullets": [
                        "Upgrade resold WatchGuard and ConnectWise MDR with AI response.",
                        "Offer premium tiered security at higher margins.",
                        "Quick win: extend current MSSP agreements.",
                    ]},
                    {"title": "Enablement Engine", "bullets": [
                        "Hire AI talent and lock in Microsoft and Salesforce partnerships.",
                        "Prove value with 2-3 anchor-client pilots in the first 90 days.",
                    ]},
                ],
            ),
            "voiceover": "So what does the plan look like? We propose three pillars, built on business we already have. First, IT Audit Automation. We can automate compliance checks and audit reporting — turning a labor-intensive service into scalable, high-margin revenue. Second, SAP Enhancement. We already run the ERP backbone for over a hundred Philippine companies. Adding AI monitoring and anomaly detection is a natural upsell. Third, AI-Powered MDR. We already resell WatchGuard and ConnectWise. Wrapping those with AI response lets us charge premium, tiered prices. And under all three, an enablement engine: hiring AI talent, signing Microsoft and Salesforce partnerships, and proving ourselves with two to three anchor-client pilots within the first ninety days.",
            "mindset": "Clear, structured, practical. This is the \"how\" — keep it simple and credible.",
        },
        {
            "type": "split_50_50",
            "args": (
                "Board Approval of AI Agent Investment Secures ICS's Next Decade",
                "Approve the AI Agent Practice now — the window is open",
                [
                    "The decision: Authorize a 90-day AI Agent Practice kickoff — team, platforms, pilots.",
                    "The cost: Small and talent-led — training and partnership fees, not heavy hardware capex.",
                    "The risk: ePLDT has launched Pilipinas AI. AI-native SIs are emerging now.",
                    "The payoff: 30-40% productivity gains for early clients; premium services margins for ICS.",
                ],
            ),
            "voiceover": "So today, I am asking the board for one decision: approve the creation of an AI Agent Practice, starting with a ninety-day kickoff. That kickoff covers three things: building a small certified team, signing Microsoft and Salesforce platform partnerships, and delivering real pilots with two to three anchor clients. The cost is modest and talent-led — training and partnership fees, not heavy capital. The risk of delay is the opposite of modest. ePLDT has already launched the country's first sovereign AI stack. AI-native integrators are entering the market as we speak. Every quarter we wait, the two-percent window gets smaller. Approve this and we protect our forty-year customer base while building premium, service-driven margins for the next decade. Thank you. I welcome your questions.",
            "mindset": "Calm, decisive close. Direct eye contact on the final ask — \"one decision.\" Gracious, open body language for Q&A.",
        },
    ]

    for data in slides_data:
        slide = prs.slides.add_slide(blank)
        renderer = {
            "hero_center": render_hero_center,
            "split_50_50": render_split_50_50,
            "metric_hero_row": render_metric_hero_row,
            "card_row_3": render_card_row_3,
            "grid_2x2": render_grid_2x2,
            "process_timeline": render_process_timeline,
        }[data["type"]]
        renderer(slide, *data["args"])
        _set_notes(slide, data["voiceover"], data["mindset"])

    prs.save("06-outputs/presentation.pptx")
    assert len(prs.slides._sldIdLst) == TOTAL_SLIDES, \
        "Expected {}, got {}".format(TOTAL_SLIDES, len(prs.slides._sldIdLst))
    print("Build OK: presentation.pptx with {} slides".format(len(prs.slides._sldIdLst)))


if __name__ == "__main__":
    main()