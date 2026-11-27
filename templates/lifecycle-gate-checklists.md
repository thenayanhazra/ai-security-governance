# Lifecycle gate checklists

Use these checklists to record sign-off at each of the five gates in the [AI and Agent Risk Framework](../framework/ai-agent-risk-framework.md#lifecycle-gates). A system cannot advance until every applicable item is checked or covered by an approved entry in the [exception register](exception-register-template.md).

**System ID:** `[AI-000]` · **System name:** `[Name]` · **Autonomy tier:** `[0 / 1 / 2 / 3]` · **Impact:** `[Low / Moderate / High / Severe]` · **EU AI Act class:** `[Class]`

---

## Gate 1: Propose (before build, purchase or SaaS toggle)

- [ ] Registered in the [AI inventory](ai-inventory-guide.md) with named business owner and technical owner ([INV-01](../framework/control-catalogue.md#inv-01), [GOV-01](../framework/control-catalogue.md#gov-01)).
- [ ] Intended purpose, target users and out-of-scope uses written down.
- [ ] Provisional autonomy tier (0–3) and impact rating (Low–Severe) assigned ([INV-02](../framework/control-catalogue.md#inv-02)).
- [ ] Confirmed not a prohibited practice under [Enterprise AI Policy §3](../policies/enterprise-ai-policy.md#3-prohibited-uses) / EU AI Act Art. 5 ([GOV-02](../framework/control-catalogue.md#gov-02)).
- [ ] Applicable regulations and EU AI Act risk classification recorded ([GOV-03](../framework/control-catalogue.md#gov-03)).
- [ ] If SaaS-embedded AI or coding agent: vendor default-off status confirmed pending review ([GOV-05](../framework/control-catalogue.md#gov-05)).

**Gate 1 sign-off:** `[Business Owner / Date]`

---

## Gate 2: Design (before connecting real data or tools)

- [ ] Architecture diagram with trust zones documented (starting from the [reference threat model](../threat-models/agentic-ai-reference-threat-model.md)).
- [ ] **Threat and impact assessment** completed and signed for Tier 2–3 or High/Severe systems ([INV-03](../framework/control-catalogue.md#inv-03)).
  - Includes DPIA (if personal data) and EU AI Act Art. 27 Fundamental Rights Impact Assessment (if high-risk deployer in scope).
- [ ] Data classes approved against the [data-use matrix](../policies/enterprise-ai-policy.md#5-data-use-matrix); DLP and log/prompt redaction designed ([DAT-01](../framework/control-catalogue.md#dat-01), [DAT-04](../framework/control-catalogue.md#dat-04)).
- [ ] Retrieval indexes, vector stores and memory enforce user ACLs and tenant isolation ([DAT-03](../framework/control-catalogue.md#dat-03), [INP-03](../framework/control-catalogue.md#inp-03)).
- [ ] Every external model provider has a completed [vendor contract checklist](vendor-contract-checklist.md) and pinned model snapshot ([SUP-03](../framework/control-catalogue.md#sup-03), [SUP-04](../framework/control-catalogue.md#sup-04)).
- [ ] Every MCP server, skill and plugin passes intake review under the [MCP supply-chain policy](../policies/mcp-and-agent-supply-chain-policy.md#4-intake-review) and is pinned/fingerprinted ([SUP-01](../framework/control-catalogue.md#sup-01), [SUP-02](../framework/control-catalogue.md#sup-02)).
- [ ] Distinct non-human agent identity, least-privilege scopes, audience-bound tokens (no token passthrough) and secrets broker designed ([IAM-01](../framework/control-catalogue.md#iam-01), [IAM-02](../framework/control-catalogue.md#iam-02), [IAM-03](../framework/control-catalogue.md#iam-03)).
- [ ] External policy enforcement layer defined for tool allow-lists, parameters, egress allow-lists, sandboxing and spend/rate caps ([ACT-02](../framework/control-catalogue.md#act-02), [ACT-03](../framework/control-catalogue.md#act-03), [ACT-04](../framework/control-catalogue.md#act-04), [ACT-06](../framework/control-catalogue.md#act-06)).
- [ ] Consequential actions catalogued with explicit human approval screens showing exact action and parameters ([ACT-01](../framework/control-catalogue.md#act-01), [HUM-02](../framework/control-catalogue.md#hum-02)).

**Gate 2 sign-off:** `[Security / Privacy / AI Risk Forum / Date]`

---

## Gate 3: Pre-release (before production traffic)

- [ ] Instruction files (`SKILL.md`, `AGENTS.md`, IDE rules, MCP configs) scanned cleanly in CI (`agentlint`, [INP-02](../framework/control-catalogue.md#inp-02)).
- [ ] Prompt-extraction and hidden-context check confirms no secrets or sole access controls live in prompts ([INP-04](../framework/control-catalogue.md#inp-04)).
- [ ] **Adversarial testing** completed for Tier 2–3 or High/Severe systems with bypass rate within appetite (`KRI-04` ≤ 5% green threshold; [TST-01](../framework/control-catalogue.md#tst-01)).
- [ ] **Accuracy, grounding and bias evaluation** meets documented acceptance criteria ([TST-04](../framework/control-catalogue.md#tst-04)).
- [ ] Cross-role / cross-tenant retrieval tests pass ([DAT-03](../framework/control-catalogue.md#dat-03)); model output encoding/validation tested ([DAT-02](../framework/control-catalogue.md#dat-02)).
- [ ] Action-level logging with agent identity, correlation ID, tamper protection and PII/secret redaction verified in staging ([OPS-01](../framework/control-catalogue.md#ops-01), [DAT-04](../framework/control-catalogue.md#dat-04)).
- [ ] **Kill switch and credential revocation** tested end-to-end under the [kill-switch runbook](../runbooks/agent-kill-switch-runbook.md) (≤ 15 min for Tier 3; [OPS-02](../framework/control-catalogue.md#ops-02)).
- [ ] AI disclosure copy, content marking (Art. 50) and agent identification headers verified ([HUM-01](../framework/control-catalogue.md#hum-01)).
- [ ] **Tier 3 only:** shadow-mode or dry-run evaluation completed with acceptable error/override rates before enabling autonomous execution.
- [ ] Final go-live approval recorded per the [approval route](../framework/ai-agent-risk-framework.md#approval-route).

**Gate 3 sign-off:** `[Approver per Approval Route / Date]`

---

## Gate 4: Operate (ongoing / periodic review)

- [ ] Continuous regression testing running in CI and blocking releases above threshold ([TST-02](../framework/control-catalogue.md#tst-02)).
- [ ] MCP tool-definition fingerprinting active and alerting/blocking on unreviewed changes ([SUP-02](../framework/control-catalogue.md#sup-02), `KRI-06`).
- [ ] Behavioural monitoring alerts triaged; spend/rate limits verified ([OPS-04](../framework/control-catalogue.md#ops-04), [ACT-06](../framework/control-catalogue.md#act-06)).
- [ ] Approval rates and decision times reviewed for rubber-stamping (`KRI-07` < 10%; [HUM-02](../framework/control-catalogue.md#hum-02)).
- [ ] Access scope review completed; over-privileged scopes removed ([IAM-02](../framework/control-catalogue.md#iam-02), `KRI-08`).
- [ ] Semi-annual kill-switch drill completed with measured time recorded ([OPS-02](../framework/control-catalogue.md#ops-02), `KRI-05`).
- [ ] Any material change (new tools, new data, higher tier, new model snapshot) routed back to Gate 2 ([SUP-04](../framework/control-catalogue.md#sup-04)).
- [ ] **Tier 3 / Severe only:** annual independent assurance report received and findings tracked ([TST-03](../framework/control-catalogue.md#tst-03)).

**Periodic review sign-off:** `[Risk Owner / Date / Next Review Date]`

---

## Gate 5: Retire (decommissioning checklist — INV-04)

Complete when withdrawing an agent, AI system, MCP server or skill:

- [ ] Traffic, schedules, webhooks and event triggers disabled; confirmed zero active invocations.
- [ ] Agent non-human identity disabled and all API keys, OAuth clients, refresh tokens and MCP credentials revoked ([IAM-01](../framework/control-catalogue.md#iam-01), [OPS-02](../framework/control-catalogue.md#ops-02)).
- [ ] Tool connections, MCP registrations, webhooks and firewall/egress allow-list entries removed.
- [ ] Long-term agent memory, caches and retrieval indexes purged or archived according to data retention rules ([INP-03](../framework/control-catalogue.md#inp-03), [INV-04](../framework/control-catalogue.md#inv-04)).
- [ ] Audit logs retained in tamper-evident archive for the required legal/regulatory retention period ([OPS-01](../framework/control-catalogue.md#ops-01)).
- [ ] Third-party provider data-deletion confirmation obtained where applicable ([SUP-03](../framework/control-catalogue.md#sup-03)).
- [ ] Inventory entry updated to `Retired` (not deleted) and any open exceptions closed ([INV-01](../framework/control-catalogue.md#inv-01)).

**Gate 5 sign-off:** `[Technical Owner & Security / Date]`
