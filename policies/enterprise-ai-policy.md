# Enterprise AI and acceptable use policy

| | |
|---|---|
| **Policy owner** | [Executive AI risk owner] |
| **Approved by** | [Board / Risk committee] |
| **Effective** | [Date] |
| **Review** | Every 12 months, and after any severity 1 or 2 AI incident or major regulatory change |
| **Related** | [AI and Agent Risk Framework](../framework/ai-agent-risk-framework.md), [control catalogue](../framework/control-catalogue.md), [MCP and agent supply-chain policy](mcp-and-agent-supply-chain-policy.md) |

## 1. Purpose

This policy sets the organisation's rules and risk appetite for building, buying, switching on and using AI systems and agents. It exists so teams can adopt AI quickly inside clear guardrails without exposing customer data, breaching law or giving software unchecked authority.

## 2. Scope

This policy applies to all employees, contractors, third parties and systems operating on the organisation's behalf, across:

- **Custom AI systems and agents** built or fine-tuned internally.
- **Third-party AI services and APIs**, including model providers, hosted agents and MCP servers.
- **SaaS-embedded AI features** (office suites, CRM, ticketing, HR and collaboration copilots).
- **Developer coding agents** and IDE assistants running on corporate devices or against corporate repositories.
- **Personal or experimental AI tools** used with corporate data, code or accounts.

## 3. Prohibited uses

The following uses are prohibited without exception:

1. **EU AI Act Article 5 prohibited practices**, including subliminal manipulation, exploitation of vulnerabilities, social scoring, untargeted scraping of facial images for recognition databases, emotion inference in the workplace or education (outside permitted safety/medical exceptions), and prohibited biometric categorisation.
2. **Unapproved autonomous high-impact decisions:** deploying a tier 3 autonomous agent with severe impact without explicit board approval, or deploying any tier 2 or 3 agent without a tested kill switch ([OPS-02](../framework/control-catalogue.md#ops-02)).
3. **Consumer AI with non-public data:** entering internal, confidential or restricted corporate data, source code or customer records into personal or consumer AI accounts that lack an approved enterprise zero-retention contract.
4. **Shadow agents and unapproved connectors:** connecting an unapproved MCP server, skill or plugin to corporate systems or data ([SUP-01](../framework/control-catalogue.md#sup-01)).
5. **Shared or personal credentials for agents:** running any production agent under an employee's personal account or a shared service credential ([IAM-01](../framework/control-catalogue.md#iam-01)).

## 4. Risk appetite and autonomy rules

1. Every AI system and agent **must** be registered in the [AI inventory](../templates/ai-inventory-guide.md) with a named business owner and technical owner before production use ([INV-01](../framework/control-catalogue.md#inv-01), [GOV-01](../framework/control-catalogue.md#gov-01)).
2. Each system **must** be classified by autonomy tier (0–3) and impact rating (Low–Severe) and approved through the [approval route](../framework/ai-agent-risk-framework.md#approval-route) before going live ([INV-02](../framework/control-catalogue.md#inv-02)).
3. Controls apply whenever a system reaches a control's minimum autonomy tier **or** its impact trigger.
4. No system may pass a lifecycle gate until the artefacts in the [lifecycle gate checklists](../templates/lifecycle-gate-checklists.md) are complete. Material changes (new tools, new data classes, a higher autonomy tier or a new model family) send the system back to Gate 2.

## 5. Data-use matrix

Only approved hosting and contract tiers may process each class of data ([DAT-01](../framework/control-catalogue.md#dat-01)):

| Data class | Examples | Consumer / free AI tools | Approved enterprise API (zero-retention, no training) | Private / VPC-hosted or approved sovereign model |
|---|---|---|---|---|
| **Public** | Published marketing, public docs, open-source code | Permitted | Permitted | Permitted |
| **Internal** | Internal policies, non-sensitive drafts, internal docs | Prohibited | Permitted | Permitted |
| **Confidential** | Commercial terms, proprietary source code, unpublished financials | Prohibited | Permitted if provider approved for Confidential | Permitted |
| **Restricted / Regulated** | Customer PII, payment data, health/HR records, security credentials | Prohibited | Permitted only with legal, privacy and AI risk forum approval | Permitted with data-use approval and DLP controls |

Secrets, API keys and authentication tokens are **never** permitted in prompts, instruction files or model context regardless of hosting tier ([IAM-03](../framework/control-catalogue.md#iam-03), [DAT-04](../framework/control-catalogue.md#dat-04)).

## 6. SaaS-embedded AI and developer coding agents

1. **SaaS AI features default to off.** Administrators **must not** switch on vendor-bundled AI assistants or agents in production SaaS tenants until the feature has been registered, its data handling and permissions verified against section 5, and approved for its tier and impact ([GOV-05](../framework/control-catalogue.md#gov-05)).
2. **Coding agents** may run only from approved vendors and configurations. Repositories that coding agents can access **must** enforce branch protection, mandatory human pull-request review, automated instruction-file scanning ([INP-02](../framework/control-catalogue.md#inp-02)) and secret scanning. Coding agents **must not** hold standing production deployment credentials.

## 7. Transparency and human oversight

1. Users and external parties **must** be informed when they interact with an AI system or receive AI-generated content, in line with applicable law including EU AI Act Article 50 ([HUM-01](../framework/control-catalogue.md#hum-01)).
2. Consequential actions require meaningful human approval showing the exact action and parameters ([ACT-01](../framework/control-catalogue.md#act-01), [HUM-02](../framework/control-catalogue.md#hum-02)). Automated output **must not** be relied on as final in high or severe impact decisions without documented human verification.

## 8. Staff responsibilities and AI literacy

1. All staff who build, approve, operate or oversee AI systems **must** complete role-based AI training within 30 days of onboarding and annually thereafter ([GOV-04](../framework/control-catalogue.md#gov-04)).
2. Staff who suspect shadow AI use, prompt injection, data leakage or unexpected agent behaviour **must** report it promptly through the AI concern and incident channel ([OPS-03](../framework/control-catalogue.md#ops-03)).

## 9. Exceptions

Exceptions to this policy follow the [exception register](../templates/exception-register-template.md). Every exception requires a documented business justification, compensating controls, an expiry date of no more than 90 days, and sign-off matching the system's [approval route](../framework/ai-agent-risk-framework.md#approval-route). No exception may be granted for section 3.1 (prohibited legal practices). All active and overdue exceptions are reported quarterly to the board (KRI-13).

## 10. Compliance and enforcement

Compliance is monitored via the [key risk indicators](../board/kri-library.md) and reported quarterly to the board. Unapproved AI integrations or agents found in use may be disabled immediately under the [kill-switch runbook](../runbooks/agent-kill-switch-runbook.md). Deliberate or repeated breaches are handled under the organisation's disciplinary policy.
