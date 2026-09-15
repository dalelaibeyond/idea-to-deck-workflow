---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  :root {
    --color-bg: #FFFFFF;
    --color-primary: #0F172A;
    --color-secondary: #2563EB;
    --color-accent: #0D9488;
    --color-surface: #F8FAFC;
    --color-text: #1E293B;
    --color-muted: #64748B;
  }
  section {
    font-family: 'Segoe UI', 'PingFang SC', sans-serif;
    padding: 40px 60px;
    background-color: var(--color-bg);
    color: var(--color-text);
  }
  section::after {
    bottom: 12px;
    right: 20px;
    font-size: 10pt;
    color: var(--color-muted);
  }
  h1 {
    color: var(--color-primary);
    font-size: 25pt;
    font-weight: 700;
    margin-bottom: 28px;
    line-height: 1.2;
  }
  .topbar {
    background: var(--color-primary);
    height: 6px;
    width: calc(100% + 120px);
    margin: -40px 0 20px -60px;
  }
  .accentbar {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 10px;
    background: var(--color-accent);
  }
  /* HERO_CENTER */
  .hero {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    height: 100%;
  }
  .hero .band {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 220px;
    background: var(--color-primary);
  }
  .hero .tag {
    position: absolute;
    top: 40px;
    left: 60px;
    color: var(--color-accent);
    font-size: 12pt;
    font-weight: 700;
    letter-spacing: 2px;
  }
  .hero h1 {
    position: relative;
    color: #FFFFFF;
    font-size: 32pt;
    margin-top: 200px;
    max-width: 860px;
  }
  .hero .subtitle {
    position: relative;
    color: var(--color-secondary);
    font-size: 18pt;
    margin-top: 12px;
  }
  .hero .takeaway {
    position: relative;
    color: var(--color-muted);
    font-size: 13pt;
    margin-top: 18px;
    max-width: 820px;
    line-height: 1.5;
  }
  .hero .meta {
    position: relative;
    color: var(--color-muted);
    font-size: 10pt;
    margin-top: 30px;
    border-top: 1px solid #CBD5E1;
    padding-top: 14px;
  }
  /* SPLIT_50_50 */
  .split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 36px;
    margin-top: 24px;
  }
  .split .left {
    background: var(--color-surface);
    border-left: 6px solid var(--color-accent);
    padding: 36px 28px;
    font-size: 20pt;
    font-weight: 700;
    color: var(--color-primary);
    line-height: 1.35;
    display: flex;
    align-items: center;
  }
  .split .right ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .split .right li {
    background: var(--color-surface);
    border-radius: 8px;
    padding: 13px 16px;
    margin-bottom: 12px;
    font-size: 13pt;
    line-height: 1.4;
  }
  .split .right li b {
    color: var(--color-primary);
  }
  /* METRIC_HERO_ROW */
  .metrics {
    display: flex;
    justify-content: space-around;
    align-items: stretch;
    gap: 24px;
    margin-top: 40px;
  }
  .metrics .card {
    flex: 1;
    background: var(--color-surface);
    border-radius: 12px;
    padding: 30px 24px;
    text-align: center;
  }
  .metrics .number {
    font-size: 40pt;
    font-weight: 700;
    color: var(--color-accent);
  }
  .metrics .label {
    font-size: 14pt;
    font-weight: 700;
    color: var(--color-primary);
    margin-top: 10px;
  }
  .metrics .context {
    font-size: 11pt;
    color: var(--color-muted);
    margin-top: 10px;
    line-height: 1.4;
  }
  /* CARD_ROW_3 */
  .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 22px;
    margin-top: 28px;
  }
  .cards .card {
    background: var(--color-surface);
    border-radius: 12px;
    padding: 24px 22px;
  }
  .cards .card.border-top {
    border-top: 6px solid var(--color-secondary);
  }
  .cards .card h3 {
    font-size: 15pt;
    font-weight: 700;
    color: var(--color-primary);
    margin-bottom: 14px;
  }
  .cards .card ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .cards .card li {
    font-size: 12pt;
    line-height: 1.4;
    margin-bottom: 10px;
    position: relative;
    padding-left: 14px;
  }
  .cards .card li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 7px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--color-accent);
  }
  /* GRID_2X2 */
  .grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 20px;
    margin-top: 22px;
  }
  .grid .quad {
    background: var(--color-surface);
    border-radius: 12px;
    padding: 18px 22px;
  }
  .grid .quad h3 {
    font-size: 15pt;
    font-weight: 700;
    margin-bottom: 10px;
  }
  .grid .quad.act h3 { color: var(--color-accent); }
  .grid .quad h3:not(.act) { color: var(--color-primary); }
  .grid .quad ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .grid .quad li {
    font-size: 12pt;
    line-height: 1.35;
    margin-bottom: 8px;
    position: relative;
    padding-left: 14px;
  }
  .grid .quad li::before {
    content: '';
    position: absolute;
    left: 0;
    top: 7px;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--color-accent);
  }
---

<!--
Voiceover: Good morning, everyone. Thank you for gathering today. For almost half a century, ICS has built its name on one thing: supporting the Philippines' most important companies with the technology they rely on. From servers and storage to SAP implementations, our name means trust. But the market is changing underneath us. The economics of the hardware business we have known are quietly eroding, year after year. Today, I want to talk about a new direction. A direction that protects everything we have built, and turns our greatest asset — our customer relationships — into the engine of our next chapter. I am going to show you why building AI Agent capabilities is the most important strategic decision ICS can make right now.
Delivery Mindset: Confident, grounded opening. Establish credibility and respect for ICS's history before introducing urgency.
-->

# Slide 1
<div class="hero">
  <div class="band"></div>
  <div class="tag">ICS STRATEGY</div>
  <h1>ICS's Hardware-Driven Model Faces Structural Margin Compression</h1>
  <div class="subtitle">48 years of client trust gives ICS the edge to lead the AI Agent era.</div>
  <div class="takeaway">The economics of traditional system integration are permanently changing. ICS must evolve from hardware reseller to AI services partner.</div>
  <div class="meta">ICS Board Strategy Meeting &nbsp;|&nbsp; AI Agent Transformation Proposal &nbsp;|&nbsp; September 2026</div>
</div>

---

<!--
Voiceover: Let's be direct about the problem. The hardware business that built ICS is no longer a source of durable profit. Across the industry, 84 percent of system integrators are now running hardware margins at 30 percent or below. Servers and storage — the heart of our CORE segment — slipped to single-digit margins this year. Industry-wide gross margins dropped by roughly three points in the last twelve months alone. And here is the structural trap: 76 percent of our installation revenue is still tied to equipment, not to the services and expertise where the value now lives. Every major industry observer says the same thing. Resale, on its own, no longer works as a business model. This is not a cyclical dip. This is a permanent reset. And it affects us directly.
Delivery Mindset: Gravitas and directness. Slow down on "permanent reset." Let the numbers land before moving forward.
-->

<div class="topbar"></div>

# Legacy Hardware Resale No Longer Sustains Profitable Growth

<div class="split">
  <div class="left">84% of integrators run hardware margins at or below 30%</div>
  <div class="right"><ul>
    <li><b>Single-digit servers:</b> Server and storage margins slipped into single digits in 2025.</li>
    <li><b>Declining gross margin:</b> Integrator gross margins fell from 41.9% to 38.6% in one year.</li>
    <li><b>Equipment-bound revenue:</b> 76% of installation revenue is tied to hardware, not services.</li>
    <li><b>The verdict:</b> "Resale stopped working as a standalone business." — DQ Channels</li>
  </ul></div>
</div>

---

<!--
Voiceover: Now, the opportunity. The global market for AI Agents is expected to grow from about eight billion dollars today to more than fifty-two billion by 2030 — a growth rate of roughly 46 percent a year. And this is not a distant Western trend. The Philippine AI market alone is projected to grow from 772 million dollars to nearly three and a half billion by 2030. Meanwhile, our own clients are hungry for AI. Seven in ten enterprises across Southeast Asia see a return on generative AI within a year. Here is the most important number for ICS: only two percent of Philippine organizations have reached what experts call the 'Integrator' stage of AI maturity. Not a single one has reached 'Leader' stage. The door is wide open. Someone will walk through it. It should be us.
Delivery Mindset: Energy rises. Momentum builds through the three numbers. Emphasize "It should be us" with conviction.
-->

<div class="topbar"></div>

# AI Agents Will Create a $52B Market by 2030 — and the Philippines Is Wide Open

<div class="metrics">
  <div class="card">
    <div class="number">$52.6B</div>
    <div class="label">Global AI Agents, 2030</div>
    <div class="context">Growing from $7.8B at 46.3% CAGR. Asia Pacific leads the curve.</div>
  </div>
  <div class="card">
    <div class="number">$3.49B</div>
    <div class="label">Philippine AI market, 2030</div>
    <div class="context">Up from $772M in 2024 — a 28.6% annual growth path.</div>
  </div>
  <div class="card">
    <div class="number">2%</div>
    <div class="label">PH at Integrator stage</div>
    <div class="context">Zero firms at AI "Leader" stage. First-mover window is open.</div>
  </div>
</div>

---

<!--
Voiceover: Why ICS? Because we are not starting from zero. First, trust. Forty-eight years of working inside the Philippines' most important companies — handling their audits, their SAP systems, their security. There is no substitute for that foundation, and no newcomer can buy it overnight. We estimate it protects our position for three to five years. Second, expertise. The work we already do — IT System Audit, SAP, and Managed Detection and Response — are exactly the use cases where AI Agents deliver thirty to forty percent productivity improvements. We do not need to invent new business; we need to make our existing business smarter. Third, the platforms have matured. Microsoft and Salesforce have built the agent engines, and they need local integrators like ICS to deploy, customize, and run them.
Delivery Mindset: Confident, assured. Slow pace. Claim the advantage without arrogance — grounded in facts.
-->

<div class="topbar"></div>

# ICS's 40 Years of Customer Trust Is the Unfair Advantage in AI Delivery

<div class="cards">
  <div class="card">
    <h3>40 Years of Trust</h3>
    <ul>
      <li>Deep relationships with the Philippines' top 1,000 enterprises.</li>
      <li>A 3-5 year window before AI-native entrants can match this.</li>
    </ul>
  </div>
  <div class="card border-top">
    <h3>Domain Expertise</h3>
    <ul>
      <li>IT Audit, SAP, and MDR are ready-made AI use cases.</li>
      <li>Agentic AI delivers 30-40% productivity gains in these areas.</li>
    </ul>
  </div>
  <div class="card">
    <h3>Platform Ecosystem</h3>
    <ul>
      <li>Microsoft Copilot Studio: 230,000+ organizations building agents.</li>
      <li>Salesforce Agentforce agents grew 119% in H1 2025. They need local SIs to deploy.</li>
    </ul>
  </div>
</div>

---

<!--
Voiceover: So what does the plan look like? We propose three pillars, built on business we already have. First, IT Audit Automation. We can automate compliance checks and audit reporting — turning a labor-intensive service into scalable, high-margin revenue. Second, SAP Enhancement. We already run the ERP backbone for over a hundred Philippine companies. Adding AI monitoring and anomaly detection is a natural upsell. Third, AI-Powered MDR. We already resell WatchGuard and ConnectWise. Wrapping those with AI response lets us charge premium, tiered prices. And under all three, an enablement engine: hiring AI talent, signing Microsoft and Salesforce partnerships, and proving ourselves with two to three anchor-client pilots within the first ninety days.
Delivery Mindset: Clear, structured, practical. This is the "how" — keep it simple and credible.
-->

<div class="topbar"></div>

# A Focused Three-Pillar Roadmap Transforms ICS from Hardware Reseller to AI SI

<div class="grid">
  <div class="quad">
    <h3>IT Audit Automation</h3>
    <ul>
      <li>Automate compliance checks and audit report generation.</li>
      <li>Turn labor-heavy service into scalable, high-margin revenue.</li>
      <li>Quick win: existing audit clients, existing tools.</li>
    </ul>
  </div>
  <div class="quad">
    <h3>SAP Enhancement</h3>
    <ul>
      <li>Add AI monitoring and anomaly detection to SAP installs.</li>
      <li>Upsell intelligent operations inside an existing customer base.</li>
      <li>Quick win: 100+ SAP customers already trust ICS.</li>
    </ul>
  </div>
  <div class="quad">
    <h3>AI-Powered MDR</h3>
    <ul>
      <li>Upgrade resold WatchGuard and ConnectWise MDR with AI response.</li>
      <li>Offer premium tiered security at higher margins.</li>
      <li>Quick win: extend current MSSP agreements.</li>
    </ul>
  </div>
  <div class="quad act">
    <h3>Enablement Engine</h3>
    <ul>
      <li>Hire AI talent and lock in Microsoft and Salesforce partnerships.</li>
      <li>Prove value with 2-3 anchor-client pilots in the first 90 days.</li>
    </ul>
  </div>
</div>

---

<!--
Voiceover: So today, I am asking the board for one decision: approve the creation of an AI Agent Practice, starting with a ninety-day kickoff. That kickoff covers three things: building a small certified team, signing Microsoft and Salesforce platform partnerships, and delivering real pilots with two to three anchor clients. The cost is modest and talent-led — training and partnership fees, not heavy capital. The risk of delay is the opposite of modest. ePLDT has already launched the country's first sovereign AI stack. AI-native integrators are entering the market as we speak. Every quarter we wait, the two-percent window gets smaller. Approve this and we protect our forty-year customer base while building premium, service-driven margins for the next decade. Thank you. I welcome your questions.
Delivery Mindset: Calm, decisive close. Direct eye contact on the final ask — "one decision." Gracious, open body language for Q&A.
-->

<div class="topbar"></div>

# Board Approval of AI Agent Investment Secures ICS's Next Decade

<div class="split">
  <div class="left">Approve the AI Agent Practice now — the window is open</div>
  <div class="right"><ul>
    <li><b>The decision:</b> Authorize a 90-day AI Agent Practice kickoff — team, platforms, pilots.</li>
    <li><b>The cost:</b> Small and talent-led — training and partnership fees, not heavy hardware capex.</li>
    <li><b>The risk:</b> ePLDT has launched Pilipinas AI. AI-native SIs are emerging now.</li>
    <li><b>The payoff:</b> 30-40% productivity gains for early clients; premium services margins for ICS.</li>
  </ul></div>
</div>

<div class="accentbar"></div>