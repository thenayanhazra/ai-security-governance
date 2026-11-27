# AI provider contract and due-diligence checklist

Use before signing or renewing contracts with model providers, hosted AI platforms, SaaS vendors with AI features or commercial MCP server providers ([SUP-03](../framework/control-catalogue.md#sup-03), [SUP-04](../framework/control-catalogue.md#sup-04)).

**Provider:** `[Name]` · **Service / Models:** `[Details]` · **Max approved data class:** `[Public / Internal / Confidential / Restricted]` · **Reviewed by:** `[Legal / Privacy / Security]` · **Date:** `[Date]`

## 1. Data protection and model training

| # | Requirement | Required for | Status | Contract reference / notes |
|---|---|---|---|---|
| 1 | **No training on customer data:** provider contractually commits not to train, fine-tune or improve models using customer prompts, completions, tool outputs or uploaded files. | Internal+ | [ ] | |
| 2 | **Zero data retention (ZDR) or bounded retention:** prompts and outputs are not retained beyond request processing (or retention period and abuse-monitoring scope are strictly bounded and documented). | Confidential+ | [ ] | |
| 3 | **Data residency and transfers:** processing and storage locations are stated; valid transfer mechanisms (e.g. EU SCCs) cover cross-border transfers. | Restricted / EU | [ ] | |
| 4 | **Deletion on termination:** customer data, fine-tuned weights, embeddings and caches are deleted within a defined SLA upon request or contract end, with written confirmation. | Internal+ | [ ] | |
| 5 | **Sub-processors:** complete list of sub-processors (including upstream model providers) with advance notice (≥ 30 days) and right to object. | Confidential+ | [ ] | |

## 2. Security, incidents and assurance

| # | Requirement | Required for | Status | Contract reference / notes |
|---|---|---|---|---|
| 6 | **Security incident notification:** provider notifies customer within a binding SLA (e.g. ≤ 24–48 hours) of confirmed security incidents, data leaks or compromised model/MCP components. | Internal+ | [ ] | |
| 7 | **Audit and assurance rights:** current SOC 2 Type II / ISO 27001 (and ISO/IEC 42001 where held) reports provided annually; right to audit or review penetration-test summaries. | Confidential+ | [ ] | |
| 8 | **Authentication & MCP security:** supports SSO/SAML, RBAC, audit-log export and—for remote MCP servers—[MCP policy §3.3](../policies/mcp-and-agent-supply-chain-policy.md#33-authentication-and-authorisation-for-remote-mcp-servers) (audience-bound tokens, RFC 8707, PKCE, no token passthrough). | Tier 1+ / Confidential+ | [ ] | |
| 9 | **SaaS AI opt-in control:** admin controls allow disabling AI features tenant-wide or per group so vendor AI rollouts do not activate unreviewed ([GOV-05](../framework/control-catalogue.md#gov-05)). | SaaS vendors | [ ] | |

## 3. Model lifecycle, regulatory alignment and exit

| # | Requirement | Required for | Status | Contract reference / notes |
|---|---|---|---|---|
| 10 | **Model version pinning and change notice:** provider supports pinned model snapshots and gives advance notice (≥ 30–60 days) before deprecating a snapshot or making material behaviour/safety changes ([SUP-04](../framework/control-catalogue.md#sup-04)). | Tier 1+ / High+ | [ ] | |
| 11 | **EU AI Act value-chain allocation (Art. 25):** provider supplies required technical documentation, intended-use instructions, GPAI disclosures (Art. 53) and serious-incident cooperation where applicable. | High / Severe / EU | [ ] | |
| 12 | **IP ownership and indemnity:** customer owns inputs and outputs; provider provides IP infringement indemnity for unmodified model outputs where commercially standard. | Confidential+ | [ ] | |
| 13 | **Exit and portability:** customer can export prompts, configurations, fine-tuning datasets, embeddings and logs in open formats without punitive lock-in (supports operational resilience / DORA). | High / Severe | [ ] | |

## Decision

- [ ] **Approved** for data classes up to `[Class]` and autonomy tiers up to `[Tier]`
- [ ] **Approved with conditions / exception** (record in [exception register](exception-register-template.md), ID: `[EX-000]`)
- [ ] **Rejected** (log reason in procurement record)

**Legal sign-off:** `[Name / Date]` · **Security sign-off:** `[Name / Date]`
