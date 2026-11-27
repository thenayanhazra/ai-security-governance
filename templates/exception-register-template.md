# AI risk exception register template

Tracks temporary exceptions to the [Enterprise AI Policy](../policies/enterprise-ai-policy.md), the [MCP and agent supply-chain policy](../policies/mcp-and-agent-supply-chain-policy.md) or the [control catalogue](../framework/control-catalogue.md). Overdue entries drive `KRI-13` in the [KRI library](../board/kri-library.md).

## Rules

1. **Time-boxed:** maximum duration is **90 days**. Permanent waivers are not permitted; if a control genuinely does not apply, record a formal scope exclusion instead.
2. **Compensating controls required:** every request must state what limits the blast radius while the gap remains open.
3. **Approval authority:** AI Risk Forum for Tier 0–2; Executive AI Risk Owner for Tier 3 or Severe impact. No exception may be granted for prohibited legal practices (EU AI Act Art. 5).
4. **Renewal:** one renewal (up to 90 days) requires documented remediation progress and re-approval. A second renewal escalates automatically to the Executive AI Risk Owner and appears in the quarterly [board report](../board/ai-risk-board-report-template.md).

## Exception request form

- **Exception ID:** `[EX-2026-001]`
- **System / Component ID:** `[AI-000]` (from the [AI inventory](ai-inventory-guide.md))
- **Autonomy tier & impact:** `[Tier / Impact]`
- **Control or policy clause:** `[e.g. IAM-01, SUP-02, MCP Policy §3.3]`
- **Requester (Business Owner):** `[Name]` · **Remediation Owner (Technical Owner):** `[Name]`
- **Business justification:** `[Why the control cannot be met today]`
- **Compensating controls:** `[Specific runtime, monitoring or scope restrictions in place]`
- **Remediation plan & target date:** `[Concrete engineering/contract fix and date]`
- **Requested expiry date (≤ 90 days):** `[YYYY-MM-DD]`
- **Approver & sign-off date:** `[AI Risk Forum / Executive AI Risk Owner, YYYY-MM-DD]`

## Register

| ID | System | Tier / Impact | Control / Policy | Compensating controls | Owner | Approved | Expires | Status |
|---|---|---|---|---|---|---|---|---|
| EX-2026-001 | AI-004 (Complaints Agent) | Tier 2 / High | [SUP-02](../framework/control-catalogue.md#sup-02) | Vendor MCP server locked to static URL; daily manual schema diff until automated fingerprinting goes live | Head of Third-Party Risk | 2026-09-15 | 2026-11-15 | Open (illustrative) |
| EX-2026-002 | AI-006 (SecOps Agent) | Tier 3 / High | [OPS-02](../framework/control-catalogue.md#ops-02) | Secondary break-glass network ACL in place while migrating to central identity broker | Head of Platform Eng | 2026-10-20 | 2027-01-18 | Open (illustrative) |
