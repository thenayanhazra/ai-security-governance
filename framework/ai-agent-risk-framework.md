# AI and Agent Risk Framework

A practical framework for governing AI systems that act, not only those that answer. It classifies each system by how much it can do without a person, sets the controls that follow from that, and gives leadership a consistent way to approve, measure and stop it.

It is written to sit alongside an existing security and risk programme. Where an organisation already has a risk taxonomy, a change process or an incident process, this framework adds the AI-specific parts and leaves the rest alone.

## Principles

1. **Govern authority, not intelligence.** The risk in an agent comes from what it is allowed to do: the tools, data and permissions it holds. A modest model with broad access is more dangerous than a capable one with none.
2. **Every input is a possible instruction.** Documents, web pages, emails, tool results and messages from other agents can all carry commands. Nothing an agent reads should be able to raise what it is allowed to do.
3. **Controls live outside the model.** A system prompt is guidance, not a boundary. Limits on tools, destinations, spend and data are enforced by components the model cannot change.
4. **People approve consequences, not conversations.** Human review is reserved for actions that matter, and shows exactly what will happen. Approval that is asked for too often becomes a reflex.
5. **If it cannot be stopped quickly, it cannot run alone.** No agent acts autonomously until it can be paused, its access revoked and its recent actions listed within minutes.

## Scope

The framework covers any AI capability the organisation builds, buys or switches on inside another product:

- **AI systems:** applications that use a model to generate content, classify or decide.
- **Agents:** systems that use a model to plan and take actions through tools.
- **Components:** models, MCP servers, skills, plugins, retrieval indexes and agent memory.

It applies whether the model is hosted by a provider, run internally or embedded in a SaaS product.

## Autonomy tiers

The tier describes what a system can do without a person approving each action. It is the main driver of which controls apply.

| Tier | Name | What the system can do | Example |
|---|---|---|---|
| 0 | Assist | Produces content or recommendations. A person decides whether and how to use them. No tools with side effects. | Drafting assistant; meeting summariser |
| 1 | Retrieve | Reads from systems through tools, without changing anything. A person acts on the result. | Knowledge assistant over internal documents; read-only analytics agent |
| 2 | Act with approval | Takes actions through tools. Consequential actions wait for a person to approve the specific action. | Support agent that drafts refunds for an agent to approve; coding agent that opens pull requests |
| 3 | Act autonomously | Takes consequential actions without approval of each one, within limits set by policy. | Agent that remediates security alerts; agent that books travel within a budget |

A system takes the tier of its most capable path. An assistant that is read-only except for one tool that sends email is tier 2 or 3, depending on whether that email needs approval.

## Impact rating

The impact rating describes the worst credible outcome if the system is misused or misbehaves, assuming its controls fail.

| Rating | Typical indicators |
|---|---|
| Low | Internal, non-sensitive data. Errors are visible and easily corrected. |
| Moderate | Confidential data, or actions that are reversible with effort. Limited external visibility. |
| High | Personal, financial or regulated data; actions that affect customers, money or access; external communications in the organisation's name. |
| Severe | Safety, legal rights, large financial loss, or actions that cannot be reversed. Includes high-risk uses under the EU AI Act. |

## Approval route

Tier and impact together decide who must approve a system before it goes live, and how often it is reviewed.

| | Low | Moderate | High | Severe |
|---|---|---|---|---|
| **Tier 0** | Team lead | Team lead | AI risk forum | AI risk forum |
| **Tier 1** | Team lead | AI risk forum | AI risk forum | Executive risk owner |
| **Tier 2** | AI risk forum | AI risk forum | Executive risk owner | Executive committee |
| **Tier 3** | AI risk forum | Executive risk owner | Executive committee | Not permitted without board approval |

Review frequency follows the same pattern: annually for the top-left of the table, quarterly for anything approved by the executive risk owner or above.

## Risk domains

Ten domains organise the [control catalogue](control-catalogue.md). Each describes a way AI systems fail and the controls that address it.

| Domain | What goes wrong | Example |
|---|---|---|
| Governance and accountability | No one owns the decision, so no one makes it well. | An agent is deployed by a team that assumed security had approved it. |
| Inventory and classification | The organisation cannot govern what it cannot see. | A department connects a public MCP server to a production agent without telling anyone. |
| Supply chain | A component behaves differently from what was reviewed. | A popular MCP server changes its tool description after approval to add a hidden instruction. |
| Agent identity and authority | Actions cannot be attributed, or the agent holds more power than the task needs. | An agent runs under a developer's personal token with access to every repository. |
| Input and context integrity | Content the agent reads redirects what it does. | A support ticket contains instructions that make the agent export the customer list. |
| Action and tool control | The agent takes an action it should not, or takes it too many times. | A coding agent runs a destructive command it found in a README. |
| Data protection | Sensitive data reaches a model, tool or destination it should not. | An agent renders a markdown image whose URL carries the conversation to an outside server. |
| Monitoring and response | Misbehaviour goes unnoticed, or cannot be stopped once noticed. | A runaway agent spends a month's API budget overnight. |
| Testing and assurance | Defences are assumed rather than shown to work. | A prompt change silently removes the instruction that blocked data export. |
| Human oversight and transparency | People are either out of the loop or in it only for show. | Reviewers approve every request in under two seconds. |

## Lifecycle gates

Controls are checked at five points. A system cannot pass a gate until the artefacts for that gate exist.

| Gate | When | Required artefacts | Key controls |
|---|---|---|---|
| 1. Propose | Before any build or purchase | Inventory entry; intended purpose; provisional tier and impact | [INV-01](control-catalogue.md#inv-01), [INV-02](control-catalogue.md#inv-02), [GOV-03](control-catalogue.md#gov-03) |
| 2. Design | Before integration with real data or tools | Threat model; data-use approval; tool and permission list; component intake records | [INV-03](control-catalogue.md#inv-03), [SUP-01](control-catalogue.md#sup-01), [IAM-02](control-catalogue.md#iam-02), [DAT-01](control-catalogue.md#dat-01) |
| 3. Pre-release | Before production | Adversarial test results against thresholds; logging and kill switch verified; approval per the route above | [TST-01](control-catalogue.md#tst-01), [OPS-01](control-catalogue.md#ops-01), [OPS-02](control-catalogue.md#ops-02), [ACT-01](control-catalogue.md#act-01) |
| 4. Operate | Continuously | Monitoring alerts; regression test trend; change reviews; periodic re-approval | [OPS-04](control-catalogue.md#ops-04), [TST-02](control-catalogue.md#tst-02), [SUP-02](control-catalogue.md#sup-02) |
| 5. Retire | When the system is withdrawn | Credentials revoked; memory and indexes purged or archived; inventory updated | [INV-04](control-catalogue.md#inv-04), [INP-03](control-catalogue.md#inp-03), [INV-01](control-catalogue.md#inv-01) |

Any material change (new tools, new data, a higher tier, a different model) sends the system back to gate 2.

## Roles

| Role | Accountable for |
|---|---|
| Board or risk committee | Approving AI risk appetite and the AI policy; receiving the quarterly AI risk report |
| Executive AI risk owner | Running the framework; approving higher-risk systems; reporting to the board. Often the CISO or CRO. |
| AI risk forum | Cross-functional approval body: security, privacy, legal, architecture and the business |
| Business owner | The purpose, value and outcomes of a specific system, and accepting its residual risk |
| Technical owner | Building and operating the system within its approved tier and controls |
| Security | Threat modelling, adversarial testing, monitoring and incident response |
| Legal and privacy | Regulatory classification, data-use approval and contractual terms |
| Internal audit | Independent assurance that controls operate as described |

## Measuring and reporting

- [Key risk indicators](../board/kri-library.md) turn the framework into numbers that can be tracked against appetite.
- The [board report template](../board/ai-risk-board-report-template.md) shows how those numbers reach the board, with a [worked example](../board/example-board-report-q3-2026.md).

## Relationship to standards

Each control maps to NIST AI RMF, ISO/IEC 42001, the EU AI Act, the OWASP Top 10 lists for LLM and agentic applications, and MITRE ATLAS. See the [crosswalk](../crosswalk/crosswalk.md). The framework does not replace those standards; it turns them into decisions an organisation can make and evidence it can show.
