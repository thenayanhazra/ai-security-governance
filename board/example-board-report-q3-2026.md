# Example: AI risk report, Q3 2026

> **Illustrative only.** A completed version of the [board report template](ai-risk-board-report-template.md) for a fictional mid-sized financial services firm operating in the EU. The organisation, figures and events are invented to show the level of detail intended.

---

## AI risk report: Q3 2026

**Prepared by:** Chief Information Security Officer (executive AI risk owner) · **For:** Board Risk Committee · **Date:** 20 October 2026

### 1. Summary

AI use remains within appetite overall, but the number of agents that can act on customer accounts doubled this quarter and our ability to stop them quickly has not kept pace. One indicator is red: our slowest tier 3 agent took 52 minutes to stop in September's exercise against a 15-minute target. We ask the committee to approve a pause on new tier 3 deployments until that is fixed, expected by the end of January.

**Overall position:** Approaching limit

### 2. Exposure

| | Q2 2026 | Q3 2026 |
|---|---|---|
| AI systems and agents in use | 41 | 58 |
| of which tier 2 (act with approval) | 9 | 14 |
| of which tier 3 (act autonomously) | 2 | 4 |
| High or severe impact systems | 6 | 9 |
| Third-party AI providers and MCP servers approved | 17 | 26 |

Growth came mainly from the customer operations programme, which moved two complaint-handling agents and one payments-exception agent into production.

### 3. Indicators against appetite

| Indicator | Appetite | Q2 | Q3 | Status |
|---|---|---|---|---|
| Inventory coverage | ≥ 98% | 94% | 98.5% | Green |
| Prompt injection bypass rate (median, tier 2 and 3) | ≤ 5% | 9% | 6% | Amber |
| Time to stop a tier 3 agent | ≤ 15 min | 12 min | 52 min | Red |
| Unreviewed MCP tool changes | 0 | Not measured | 1 (under 24 hours) | Amber |
| Rubber-stamp rate | < 10% | 31% | 14% | Amber |
| AI security incidents | No severity 1 or 2 | None | One severity 3 | Green |

**Time to stop (red).** The new payments-exception agent uses credentials issued by a separate platform team, and revoking them required a manual change request. *Action:* move the agent to the central identity broker so revocation is automatic. *Owner:* Head of Platform Engineering. *Expected green:* 31 January 2027.

**Bypass rate (amber).** Improved from 9% to 6% after we separated retrieved documents from instructions in the complaints agents. The remaining failures are attacks written in languages other than English. *Owner:* AI Security Lead. *Expected green:* next quarter.

**Unreviewed tool change (amber).** First quarter this has been measurable. A vendor updated a document-search tool's description; it was blocked automatically and cleared the next day.

**Rubber-stamp rate (amber).** Down from 31% after we cut the number of approval prompts in the refunds agent by two-thirds. Further reduction depends on the redesign in risk 3 below.

### 4. Top risks

| Risk | Rating | Trend | Owner | Next action and date |
|---|---|---|---|---|
| 1. An autonomous agent acting on customer accounts cannot be stopped quickly if it misbehaves | High | ↑ | Head of Platform Engineering | Central credential revocation for all tier 3 agents, 31 Jan 2027 |
| 2. Instructions hidden in customer emails or documents redirect the complaints agents | Medium | ↓ | AI Security Lead | Add multilingual attacks to release testing, 15 Dec 2026 |
| 3. Staff approve agent actions without reading them | Medium | ↓ | COO, Customer Operations | Redesign approval screen to show amount and payee first, 30 Nov 2026 |
| 4. A third-party MCP server changes behaviour after approval | Medium | → | Head of Third-Party Risk | Extend fingerprinting to all 26 approved servers, 15 Nov 2026 |
| 5. High-risk classification under the EU AI Act is applied inconsistently across business lines | Medium | → | General Counsel | Complete classification review of all 9 high-impact systems, 31 Mar 2027 |

### 5. Incidents and near misses

One severity 3 incident. A test version of the internal knowledge assistant displayed a staff member's salary band, retrieved from an HR document that had been indexed in error. No customer data was involved. The document has been removed, and HR folders are now excluded from indexing by default.

### 6. Regulatory and standards horizon

| Date | Change | Effect on us | Readiness |
|---|---|---|---|
| 2 Dec 2026 | EU AI Act: new prohibited practices added by the Digital Omnibus take effect; legacy generative systems must apply machine-readable marking (Art. 50(2)) | Marketing content generator needs output marking | On track |
| 2 Dec 2027 | EU AI Act: high-risk obligations for Annex III systems apply (deferred from August 2026) | Creditworthiness assessment model is in scope; risk management, logging and human oversight evidence required | On track |
| Not yet announced | Revised NIST AI RMF (NIST has said version 1.0 is under revision) | Our control mapping will need updating; no change to obligations | Monitoring |

### 7. Decisions requested

1. **Pause new tier 3 deployments until the time-to-stop indicator is green.** *Recommendation:* approve. *Trade-off:* the planned autonomous fraud-triage agent moves from December to February. *If not decided:* new tier 3 agents would go live with the same revocation gap as the payments-exception agent.
