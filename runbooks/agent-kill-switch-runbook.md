# Agent kill-switch and credential revocation runbook

Operationalises [OPS-02](../framework/control-catalogue.md#ops-02) and produces measured times for `KRI-05` (*Time to stop an agent*) in the [KRI library](../board/kri-library.md).

**Target SLA:** **≤ 15 minutes** for Tier 3 agents (and Severe-impact systems); **≤ 60 minutes** for Tier 2 agents. Clock starts when the decision to stop is made and ends only when the agent has stopped acting **and** its credentials no longer work.

## 1. Triggers

Execute this runbook immediately if any of the following occur:
- Confirmed or suspected prompt injection causing unauthorised tool calls or data exfiltration.
- A connected MCP server fails tool-definition fingerprint verification ([SUP-02](../framework/control-catalogue.md#sup-02)) or shows rug-pull behaviour.
- Runaway loop, abnormal spend spike or unexpected destructive actions ([ACT-06](../framework/control-catalogue.md#act-06), [OPS-04](../framework/control-catalogue.md#ops-04)).
- Compromised agent credential or suspected goal drift.

## 2. Emergency halt procedure

Complete steps 1–6 in order. Record exact UTC timestamps for every step.

| Step | Action | Owner | Verification |
|---|---|---|---|
| **1. Pause execution** | Toggle the agent feature flag / disable scheduled triggers, queues, webhooks and API gateway route in the orchestrator or policy enforcement layer. | Technical Owner / On-Call | Zero new tasks queued or running. |
| **2. Revoke identity & tokens** | Disable the agent's non-human identity ([IAM-01](../framework/control-catalogue.md#iam-01)), revoke active OAuth/OIDC tokens, rotate or invalidate secrets-broker leases, and revoke MCP client registrations ([IAM-02](../framework/control-catalogue.md#iam-02)). | Platform / IAM On-Call | Test call with previous token returns `401`/`403`. |
| **3. Block egress & tools** | Apply deny-all rule for the agent identity at the policy enforcement layer ([ACT-02](../framework/control-catalogue.md#act-02)) and remove/quarantine affected MCP servers. | Platform / Security | Policy layer logs show `DENY` on test invocation. |
| **4. Kill in-flight sandboxes** | Terminate active code-execution sandboxes and sub-agent sessions spawned by the orchestrator ([ACT-03](../framework/control-catalogue.md#act-03), [ACT-05](../framework/control-catalogue.md#act-05)). | Platform On-Call | Zero active containers/jobs for agent ID. |
| **5. Enumerate recent actions** | Query tamper-protected action logs ([OPS-01](../framework/control-catalogue.md#ops-01)) by agent identity and correlation IDs for the affected window; list every external write, message, transfer or data read. | Security | Action timeline exported and preserved. |
| **6. Escalate & hand off** | Open or update the security incident ticket under the [AI incident response playbooks](ai-incident-response-playbooks.md) and notify the Business Owner and Executive AI Risk Owner. | Security | Incident commander assigned. |

## 3. Resumption criteria

A halted agent **must not** be re-enabled until:
1. Root cause is identified and remediated (e.g. poisoned tool removed, prompt/policy patched, compromised memory purged per [INP-03](../framework/control-catalogue.md#inp-03)).
2. Fresh credentials are issued under least privilege.
3. Regression and adversarial tests pass ([TST-01](../framework/control-catalogue.md#tst-01), [TST-02](../framework/control-catalogue.md#tst-02)).
4. Re-enablement is signed off by Security and the Business Owner (plus the Executive AI Risk Owner for severity 1–2 incidents).

## 4. Semi-annual exercise log (KRI-05 evidence)

Run an unannounced or tabletop-plus-live halt drill **at least twice a year** for every Tier 3 agent (and any Severe-impact system). An exercise that has not occurred within 6 months scores **Red** on `KRI-05`.

| Date (UTC) | System ID | Decision time (T0) | Execution paused | Credentials verified invalid (T1) | Action list exported | Total time (T1 − T0) | KRI-05 status | Gaps & follow-up actions |
|---|---|---|---|---|---|---|---|---|
| 2026-09-18 | AI-006 | 10:00:00 | 10:03:12 | 10:11:40 | 10:14:05 | 11m 40s | Green | None (illustrative) |
