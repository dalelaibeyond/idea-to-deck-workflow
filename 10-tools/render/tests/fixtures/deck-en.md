---
total_slides: 6
audience: "Meridian Cloud board of directors and executive sponsors"
core_objective: "Approve the two-year platform consolidation program and its funding envelope"
scenario: "Quarterly board strategy review"
---

## Slide 1

```yaml slide
layout: HERO_CENTER
action_title: "Meridian Runs on Nine Platforms — Consolidation Is Now a Board-Level Risk"
args:
  kicker: "MERIDIAN CLOUD · BOARD BRIEFING"
  subtitle: "One platform, one operating model, four quarters to deliver."
  takeaway: "Every additional platform we operate adds cost, latency, and audit surface. Consolidation is the cheapest risk reduction available to this board."
  meta: "Meridian Cloud Board Review  |  Platform Consolidation Program  |  Q3 2026"
voiceover: |
  Good morning. Three years ago we made a pragmatic call: ship fast, buy what we need, and integrate later. Nine platforms later, the bill has arrived. We spend more on glue code than on any single product line, and every audit cycle starts from scratch. Today I am asking the board to approve one platform, one operating model, and the four quarters it takes to get there. This is not a technology refresh. It is the cheapest risk reduction available to this company.
mindset: "Confident, grounded opening. Establish the cost of delay before naming the ask."
```

## Slide 2

```yaml slide
layout: SPLIT_50_50
action_title: "Platform Sprawl Now Consumes 31% of Engineering Capacity"
args:
  left_anchor: "Nine platforms absorb 31% of engineering capacity in maintenance and glue work"
  right_bullets:
    - "Integration tax: 214 internal adapters, 61% owned by teams that have rotated off."
    - "Release drag: cross-platform features ship 3.4x slower than single-platform ones."
    - "Audit surface: four of nine platforms failed the last SOC 2 evidence cycle."
    - "The verdict: \"Complexity is a loan — someone always pays it back.\" — internal architecture review"
voiceover: |
  Let me quantify the sprawl. Almost a third of our engineering capacity goes to keeping nine platforms talking to each other. Two hundred and fourteen internal adapters, most owned by people who have already rotated to other teams. Cross-platform features take three point four times longer to ship. And in the last SOC 2 cycle, four platforms could not produce complete evidence without manual remediation. Our own architecture review said it best: complexity is a loan, and someone always pays it back. That someone is us, this year.
mindset: "Direct and quantitative. Slow down on the final quote."
```

## Slide 3

```yaml slide
layout: METRIC_HERO_ROW
action_title: "Consolidation Frees $18M and Cuts Audit Surface by Two-Thirds"
args:
  metrics:
    - number: "$18.2M"
      label: "Annual run-rate savings"
      context: "Licenses, glue engineering, and incident toil from FY27 onward."
    - number: "9 → 2"
      label: "Platforms after consolidation"
      context: "One primary runtime plus one regulated-workload enclave."
    - number: "-67%"
      label: "SOC 2 evidence scope"
      context: "Fewer platforms, fewer control matrices, faster audits."
voiceover: |
  The upside is concrete. Eighteen point two million in annual run-rate savings once the program completes. We go from nine platforms to two — a primary runtime, and a small enclave for regulated workloads. And because audit scope scales with platform count, our SOC 2 evidence surface shrinks by two thirds. These numbers are conservative: they exclude the revenue upside from shipping faster.
mindset: "Momentum builds across the three numbers. Land on the conservative framing."
```

## Slide 4

```yaml slide
layout: CARD_ROW_3
action_title: "Three Verified Capabilities De-Risk the Consolidation Path"
args:
  cards:
    - header: "Proven Migration Playbook"
      bullets:
        - "Two business units migrated in the FY25 pilot with zero data loss."
        - "Playbook covers cutover, rollback, and dual-run verification."
    - header: "Portable Core Services"
      bullets:
        - "Identity, billing, and event bus already run platform-agnostic."
        - "78% of application teams consume them exclusively via standard APIs."
    - header: "Named Retention Pool"
      bullets:
        - "Original platform owners contracted for 20% time through FY27."
        - "Escrow runbooks and on-call rotation handed over per migration wave."
voiceover: |
  Why do we believe this is executable? Three reasons. First, we have run the playbook — two business units migrated in the pilot with zero data loss. Second, the core services that matter, identity, billing, and the event bus, already run platform-agnostic. Third, we have retained the people who built these platforms, contractually, through the end of the program. De-risking is not a promise here. It is a plan with names on it.
mindset: "Assured and factual. Emphasize 'names on it'."
```

## Slide 5

```yaml slide
layout: GRID_2X2
action_title: "A Four-Workstream Program Delivers Consolidation in Four Quarters"
args:
  quadrants:
    - title: "Workstream: Migrate"
      bullets:
        - "Wave 1: internal tooling and low-risk services, Q1."
        - "Waves 2-3: customer-facing workloads, Q2-Q3."
    - title: "Workstream: Decommission"
      bullets:
        - "Retire one platform per completed wave, no shelf-ware."
        - "License terminations timed to contract renewal dates."
    - title: "Workstream: Harden"
      bullets:
        - "Regulated enclave passes SOC 2 and regional data rules."
        - "Chaos and load testing before each customer-facing wave."
    - title: "Workstream: Enable"
      bullets:
        - "Dedicated migration guild: 12 engineers, rotating seats."
        - "Executive checkpoint at each quarter boundary."
voiceover: |
  The program has four workstreams. Migrate moves workloads in three waves, starting with internal tooling where blast radius is smallest. Decommission retires a platform at the end of every wave — no shelf-ware, licenses terminated at renewal dates. Harden takes the regulated enclave through SOC 2 and regional data rules ahead of customer-facing waves. And Enable staffs a rotating migration guild with an executive checkpoint every quarter. Four workstreams, four quarters, one platform.
mindset: "Structured and calm. This is the how — keep it crisp."
```

## Slide 6

```yaml slide
layout: PROCESS_TIMELINE
action_title: "Four Checkpoints From Approval to Full Consolidation"
args:
  steps:
    - header: "Q1: Approve & Mobilize"
      summary: "Board approves funding; guild staffed; wave 1 scoped and baselined."
    - header: "Q2: Prove"
      summary: "Internal tooling migrated; first platform decommissioned; savings tracked."
    - header: "Q3: Scale"
      summary: "Customer-facing waves 2-3 executed under hardening gates."
    - header: "Q4: Complete"
      summary: "Final retirement, audit recertification, savings at run-rate."
voiceover: |
  Here is the timeline the board is approving today. Quarter one, funding and mobilization. Quarter two, proof: internal tooling migrated and the first platform retired. Quarter three, we scale to customer-facing workloads under the hardening gates. Quarter four, final retirement and audit recertification, with savings at full run-rate. Each quarter ends with a named checkpoint where this board can see progress and stop the program if we miss. I am asking for your approval to start quarter one today.
mindset: "Decisive close. Pause before the final ask."
```
