# AI incident response playbooks

Operationalises [OPS-03](../framework/control-catalogue.md#ops-03) and aligns incident severity with `KRI-11` in the [KRI library](../board/kri-library.md). Designed to plug into an existing security incident response process.

## 1. Severity classification

| Severity | Definition | Examples | Escalation |
|---|---|---|---|
| **Severity 1 (Critical)** | Confirmed unauthorised consequential action, broad leakage of Restricted/customer data, safety/fundamental-rights harm, or compromised production MCP server/model affecting multiple systems. | Agent exfiltrates customer PII via tool call; autonomous payments agent executes fraudulent transfers; supply-chain rug pull executes across prod agents. | Executive AI Risk Owner + Legal/DPO within 1 hour; Board Chair notified. |
| **Severity 2 (High)** | Contained unauthorised tool invocation, targeted Confidential data exposure, persistent memory/RAG poisoning, or active bypass of policy/approval gates without broad external impact. | Indirect injection triggers email to external address (blocked or single record); poisoned memory entry alters future sessions; Tier 3 kill switch fails SLA. | Security Lead + Business Owner + Legal within 4 hours; reported to Board in quarterly pack. |
| **Severity 3 (Medium)** | Internal-only exposure of non-customer data, blocked/contained prompt injection with policy gap, or misconfigured retrieval scope caught internally. | Internal assistant surfaces restricted HR document to unauthorised staff member; runaway loop halted by spend cap. | Security + Technical Owner within 1 business day. |
| **Severity 4 (Low / Near miss)** | Policy violation or anomaly with no data or action impact; unapproved shadow AI tool found and disconnected cleanly. | Staff member connects unapproved MCP server to non-sensitive repo; benign alert spike. | Logged, remediated and tracked in quarterly trend. |

## 2. Scenario playbooks

### Playbook A: Indirect prompt injection & data exfiltration
1. **Contain:** Execute the [kill-switch runbook](agent-kill-switch-runbook.md) if exfiltration is active or tool calls cannot be bounded.
2. **Scope:** Pull action logs ([OPS-01](../framework/control-catalogue.md#ops-01)) by correlation ID; identify the untrusted source (ticket, email, web page, document, tool response) and every outbound request, email, URL or rendered markdown image ([ACT-04](../framework/control-catalogue.md#act-04)).
3. **Eradicate:** Quarantine the malicious input source; tighten input-data separation ([INP-01](../framework/control-catalogue.md#inp-01)), policy allow-lists ([ACT-02](../framework/control-catalogue.md#act-02)) and output rendering filters ([DAT-02](../framework/control-catalogue.md#dat-02)).
4. **Prevent recurrence:** Add the exact attack payload to the CI adversarial regression corpus ([TST-02](../framework/control-catalogue.md#tst-02)).

### Playbook B: Compromised or rug-pulled MCP server / instruction file
1. **Contain:** Block the component hash/URL in the central registry and policy enforcement layer across **all** agents and developer workstations ([SUP-01](../framework/control-catalogue.md#sup-01), [SUP-02](../framework/control-catalogue.md#sup-02)).
2. **Revoke:** Rotate any tokens, OAuth grants or secrets reachable by agents that loaded the component ([IAM-02](../framework/control-catalogue.md#iam-02), [IAM-03](../framework/control-catalogue.md#iam-03)).
3. **Investigate:** Diff the changed tool description, schema or instruction file (`SKILL.md`, `AGENTS.md`, IDE rules); scan repositories with `agentlint` and search logs for any actions executed after the change timestamp.
4. **Recover:** Replace only with a newly reviewed, version-pinned artefact; record vendor incident and notify upstream maintainer or community where appropriate.

### Playbook C: Runaway or rogue agent / spend spike
1. **Contain:** Trigger the [kill-switch runbook](agent-kill-switch-runbook.md) and confirm token/API spend has dropped to zero at the model provider console ([ACT-06](../framework/control-catalogue.md#act-06)).
2. **Assess impact:** Enumerate all side-effecting tool calls and downstream sub-agent fan-out ([ACT-05](../framework/control-catalogue.md#act-05)); initiate transaction reversals or rollbacks with business teams.
3. **Fix:** Add or tighten hard limits on step count, delegation depth, spend and run time outside the model, and update behavioural monitoring alerts ([OPS-04](../framework/control-catalogue.md#ops-04)).

### Playbook D: Unauthorised retrieval / cross-tenant data leak
1. **Contain:** Disable the affected retrieval connector, index or semantic cache immediately; isolate the exposed document corpus.
2. **Scope:** Query retrieval and prompt logs to determine every user or tenant who received unauthorised chunks, and whether the data was sent to an external model provider.
3. **Eradicate:** Remove mis-indexed folders/records, purge contaminated caches or agent memory ([INP-03](../framework/control-catalogue.md#inp-03)), and enforce query-time ACL/tenant filters ([DAT-03](../framework/control-catalogue.md#dat-03)).
4. **Notify:** Engage Privacy/Legal immediately to assess GDPR / breach notification obligations.

## 3. Regulatory notification timelines

Engage Legal and Privacy at triage whenever an incident involves personal data, regulated financial operations or an EU AI Act high-risk system:

| Regime | Trigger | Statutory window |
|---|---|---|
| **EU AI Act Art. 73** (serious incident — high-risk AI) | Widespread infringement or serious & irreversible disruption of critical infrastructure | **Immediately, and no later than 2 days** after establishing causal link |
| **EU AI Act Art. 73** | Death of a person | **Immediately, and no later than 10 days** |
| **EU AI Act Art. 73** | Other serious incidents (serious harm to health, fundamental rights or property/environment) | **Immediately, and no later than 15 days** |
| **GDPR Art. 33 / UK GDPR** | Personal data breach posing risk to rights and freedoms | **Without undue delay, and within 72 hours** |
| **DORA / sector rules** (if applicable) | Major ICT-related incident (financial entities) | Initial notification within **4 hours of classification** (and ≤ 24 hours of detection) |

Deployers of high-risk systems must also notify the **provider** immediately so provider reporting obligations under Art. 73 can be met.

## 4. Reporting concerns channel (ISO/IEC 42001 A.3.3)

Staff, contractors and users must have a clear, low-friction way to report AI safety, bias, privacy or misuse concerns—even when they are unsure it is a security incident:
- **Internal channel:** `[e.g. #ai-security-concerns / ai-risk@example.com / Ethics hotline category "AI System Concern"]` (anonymous option available via existing whistleblowing route).
- **Triage SLA:** Acknowledged within 1 business day by AI Risk / Security; logged with disposition and escalated to Playbooks A–D if security or regulatory impact is identified.
