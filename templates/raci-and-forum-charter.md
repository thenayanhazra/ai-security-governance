# AI risk RACI and AI risk forum charter

Operationalises [GOV-01](../framework/control-catalogue.md#gov-01) and the roles defined in the [AI and Agent Risk Framework](../framework/ai-agent-risk-framework.md#roles). Replace role titles in brackets to match your organisation.

## 1. Decision RACI

**R** = Responsible (does the work) · **A** = Accountable (signs off; exactly one per row) · **C** = Consulted · **I** = Informed

| Activity | Board / Risk Committee | Executive AI Risk Owner | AI Risk Forum | Business Owner | Technical Owner | Security | Legal & Privacy | Internal Audit |
|---|---|---|---|---|---|---|---|---|
| Approve Enterprise AI Policy & risk appetite ([GOV-02](../framework/control-catalogue.md#gov-02)) | **A** | **R** | C | I | I | C | C | I |
| Maintain AI inventory & run discovery ([INV-01](../framework/control-catalogue.md#inv-01)) | I | **A** | C | C | **R** | **R** | I | I |
| Assign autonomy tier, impact & EU AI Act class ([INV-02](../framework/control-catalogue.md#inv-02), [GOV-03](../framework/control-catalogue.md#gov-03)) | I | I | **A** | **R** | C | C | C | I |
| Approve Tier 0–1 Low-impact systems | I | I | I | **A** | **R** | I | I | I |
| Approve Tier 1 Moderate/High or Tier 2 Low/Moderate systems | I | I | **A** | **R** | **R** | C | C | I |
| Approve Tier 2 High or Tier 3 Moderate systems | I | **A** | C | **R** | **R** | C | C | I |
| Approve Tier 3 Severe systems | **A** | **R** | C | C | C | C | C | I |
| Approve MCP servers & third-party components for Tier 2–3 ([SUP-01](../framework/control-catalogue.md#sup-01)) | I | I | **A** | C | **R** | **R** | C | I |
| Review & approve AI provider contract terms ([SUP-03](../framework/control-catalogue.md#sup-03)) | I | I | C | C | I | C | **A/R** | I |
| Threat model & pre-release adversarial testing ([INV-03](../framework/control-catalogue.md#inv-03), [TST-01](../framework/control-catalogue.md#tst-01)) | I | I | **A** | C | **R** | **R** | C | I |
| Execute kill switch & semi-annual halt drills ([OPS-02](../framework/control-catalogue.md#ops-02)) | I | **A** | I | I | **R** | **R** | I | I |
| Lead AI security incident response & regulatory notice ([OPS-03](../framework/control-catalogue.md#ops-03)) | I | **A** | I | C | **R** | **R** | **R** | I |
| Approve 90-day control exceptions (Tier 0–2) | I | I | **A** | **R** | C | C | C | I |
| Approve 90-day control exceptions (Tier 3) | I | **A** | C | **R** | C | C | C | I |
| Deliver quarterly board AI risk report | I | **A/R** | C | I | I | C | C | I |
| Annual independent assurance of Tier 3 & Severe systems ([TST-03](../framework/control-catalogue.md#tst-03)) | I | I | I | C | C | C | I | **A/R** |

---

## 2. AI Risk Forum charter

### Mandate
The AI Risk Forum is the cross-functional approval and oversight body for AI systems, agents, MCP servers, SaaS-embedded AI features and policy exceptions within its delegated authority in the [approval route](../framework/ai-agent-risk-framework.md#approval-route).

### Standing members
- **Chair:** [Head of AI Risk / CISO delegate]
- **Security:** AI Security Lead / Application Security representative
- **Privacy & Legal:** Data Protection Officer / Commercial Counsel
- **Architecture & Platform:** Principal Architect / Platform Engineering Lead
- **Business & Risk:** Operational Risk representative + sponsoring Business Owner (attends for their system only)

### Quorum and decision rules
- **Quorum:** Chair + Security + Legal/Privacy + Architecture (minimum 4).
- **Decisions:** Consensus preferred; if split, any standing member may escalate to the Executive AI Risk Owner.
- **No self-approval:** A Business or Technical Owner may not vote on their own system or exception.

### Cadence and service levels
- **Standing meeting:** Fortnightly (every 2 weeks), 60 minutes.
- **Asynchronous fast-track:** Low/Moderate Tier 1 proposals and minor component updates with clean automated scans (`agentlint`, `ai-security-assessment`) may be approved asynchronously within **5 business days** if no standing member objects.
- **Full review SLA:** Complete Gate 2 / Gate 3 packs submitted at least 3 business days before the meeting receive a decision (Approve / Approve with conditions / Reject) at that session.
- **Emergency review:** Convened within 24 hours for severity 1–2 incidents, zero-day MCP vulnerabilities or urgent regulatory changes.

### Escalation and reporting
- Systems rated **Tier 2 High**, **Tier 3 Moderate** or above, and any **Tier 3 exception**, are escalated with a written Forum recommendation to the Executive AI Risk Owner, Executive Committee or Board per the approval route.
- Forum minutes, approvals, rejections and open exceptions feed the quarterly [board report](../board/ai-risk-board-report-template.md).
