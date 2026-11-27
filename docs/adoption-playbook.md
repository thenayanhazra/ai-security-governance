# Adoption playbook: 30 / 60 / 90 days and maturity rubric

How a security and risk function can adopt this governance kit in weeks rather than quarters.

## 30 / 60 / 90-day rollout

### Days 1–30: Visibility and policy foundation (Level 2)
- **Appoint ownership:** name the Executive AI Risk Owner and stand up the AI Risk Forum using the [RACI and forum charter](../templates/raci-and-forum-charter.md) ([GOV-01](../framework/control-catalogue.md#gov-01)).
- **Adopt core policies:** tailor and approve the [Enterprise AI Policy](../policies/enterprise-ai-policy.md) (including the data-use matrix and SaaS default-off rule) and the [MCP supply-chain policy](../policies/mcp-and-agent-supply-chain-policy.md) ([GOV-02](../framework/control-catalogue.md#gov-02), [GOV-05](../framework/control-catalogue.md#gov-05)).
- **Build the inventory:** populate the [AI inventory](../templates/ai-inventory-guide.md) across custom models, agents, coding agents, MCP servers and SaaS copilots; assign autonomy tiers (0–3), impact ratings and EU AI Act classes ([INV-01](../framework/control-catalogue.md#inv-01), [INV-02](../framework/control-catalogue.md#inv-02), [GOV-03](../framework/control-catalogue.md#gov-03)).
- **Turn on cheap CI checks:** add `agentlint` scanning to repositories containing `AGENTS.md`, `SKILL.md`, IDE rules or MCP configs ([INP-02](../framework/control-catalogue.md#inp-02)).

### Days 31–60: Enforcement on Tier 2–3 and High/Severe systems (Level 3)
- **Gate new releases:** enforce Gates 1–3 with the [lifecycle gate checklists](../templates/lifecycle-gate-checklists.md) and [vendor contract checklist](../templates/vendor-contract-checklist.md) ([INV-03](../framework/control-catalogue.md#inv-03), [SUP-03](../framework/control-catalogue.md#sup-03)).
- **Isolate authority:** move production agents onto distinct non-human identities, short-lived audience-bound tokens and a secrets broker ([IAM-01](../framework/control-catalogue.md#iam-01), [IAM-02](../framework/control-catalogue.md#iam-02), [IAM-03](../framework/control-catalogue.md#iam-03)).
- **Move controls outside the model:** route tool calls, egress and spend caps through an external policy layer (see the [OPA starter policy](../examples/opa/README.md)) and fingerprint approved MCP tool definitions ([ACT-02](../framework/control-catalogue.md#act-02), [SUP-02](../framework/control-catalogue.md#sup-02)).
- **Verify kill switches:** run the first live halt drill for Tier 3 agents using the [kill-switch runbook](../runbooks/agent-kill-switch-runbook.md) and record `KRI-05` ([OPS-02](../framework/control-catalogue.md#ops-02)).

### Days 61–90: Assurance and board reporting (Level 4)
- **Automate adversarial testing:** wire `ai-security-assessment` and regression fuzzing into CI using the [governance gate workflow](../examples/ci/ai-governance-gate.yml) ([TST-01](../framework/control-catalogue.md#tst-01), [TST-02](../framework/control-catalogue.md#tst-02), `KRI-04`).
- **Baseline behaviour & oversight:** turn on action-level logging with PII/secret redaction ([OPS-01](../framework/control-catalogue.md#ops-01), [DAT-04](../framework/control-catalogue.md#dat-04)), behavioural alerts ([OPS-04](../framework/control-catalogue.md#ops-04)) and approval-time monitoring (`KRI-07`, [HUM-02](../framework/control-catalogue.md#hum-02)).
- **Deliver the first board pack:** select 6–8 KRIs from the [KRI library](../board/kri-library.md) and deliver the first quarterly [board report](../board/ai-risk-board-report-template.md), including active exceptions from the [exception register](../templates/exception-register-template.md) (`KRI-13`).
- **Schedule independent assurance:** place Tier 3 and Severe-impact systems onto Internal Audit's annual assurance plan ([TST-03](../framework/control-catalogue.md#tst-03)).

## Maturity self-assessment rubric

| Level | Name | What is true |
|---|---|---|
| **1** | **Ad-hoc** | AI tools and agents adopted informally; no central inventory; reliance on system prompts and vendor defaults; board has no AI risk metrics. |
| **2** | **Visible** | Executive owner and AI Risk Forum active; Enterprise AI & MCP policies approved; inventory covers ≥ 90% of discovered AI (`KRI-01`); systems classified by tier and impact; CI instruction scanning active. |
| **3** | **Enforced** | Gates 1–5 operating; agents run with distinct non-human identities and external policy enforcement; MCP tool definitions pinned and fingerprinted (`KRI-06`); kill switches tested ≤ 60 min (`KRI-05`); vendor contracts and 90-day exceptions tracked. |
| **4** | **Assured** | Continuous adversarial and accuracy/bias regression testing blocks releases (`KRI-04`); Tier 3 kill switches verified ≤ 15 min twice yearly; rubber-stamping monitored (`KRI-07`); quarterly board pack drives investment and pause decisions; annual independent assurance on Tier 3 and Severe systems. |

## Interactive control filter

Open [`control-selector.html`](control-selector.html) in any browser to filter applicable controls, approval routes and KRIs by autonomy tier, impact rating and regulatory framework.
