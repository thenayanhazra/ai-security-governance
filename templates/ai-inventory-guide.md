# AI system and agent inventory guide

A single register covering every AI system, agent, SaaS-embedded AI feature, coding agent, model and MCP server in use ([INV-01](../framework/control-catalogue.md#inv-01), [INV-02](../framework/control-catalogue.md#inv-02), [GOV-03](../framework/control-catalogue.md#gov-03)).

Starter file with illustrative rows: [`ai-inventory-template.csv`](ai-inventory-template.csv).

## Field definitions

| Column | Required | Guidance |
|---|---|---|
| `system_id` | Yes | Stable unique identifier (`AI-001`, `AI-002`, ...) reused across threat models, logs, exceptions and audit evidence. |
| `name` | Yes | Plain-language name used in business and board reporting. |
| `type` | Yes | One of: `AI system`, `RAG assistant`, `Agent`, `Coding agent`, `SaaS-embedded`, `MCP server`, `Skill/Plugin`. |
| `status` | Yes | `Proposed`, `In design`, `Pre-release`, `Production`, `Paused`, `Retired`. |
| `business_owner` | Yes | Named person or role accountable for purpose, value and residual risk ([GOV-01](../framework/control-catalogue.md#gov-01)). |
| `technical_owner` | Yes | Named person or role accountable for operating the system within its approved controls. |
| `autonomy_tier` | Yes | `0` (Assist), `1` (Retrieve), `2` (Act with approval), `3` (Act autonomously). Takes the tier of its most capable path. |
| `impact_rating` | Yes | `Low`, `Moderate`, `High` or `Severe` — worst credible outcome if controls fail. |
| `eu_ai_act_class` | Yes | `Out of scope`, `Minimal risk`, `Limited risk (Art. 50)`, `High-risk (Annex I)`, `High-risk (Annex III)`, or `Prohibited (Art. 5)` (must be blocked). |
| `data_classes` | Yes | Highest data classes processed: `Public`, `Internal`, `Confidential`, `Restricted`. |
| `model_provider` | Yes | External provider or `Internal`. |
| `model_snapshot` | Yes | Pinned model version/snapshot ID ([SUP-04](../framework/control-catalogue.md#sup-04)), or `vendor-managed` where pinning is unavailable. |
| `mcp_servers_and_tools` | Yes | Pinned versions of connected MCP servers, skills or write-capable tools (`None` if none). |
| `kill_switch_owner` | Tier 2–3 / Severe | Role or on-call team able to pause the system and revoke credentials within SLA ([OPS-02](../framework/control-catalogue.md#ops-02)). |
| `last_assessment_date` | Tier 2–3 / High+ | Date of last approved threat and impact assessment ([INV-03](../framework/control-catalogue.md#inv-03)). |
| `next_review_date` | Yes | Annually for team-lead / forum-approved systems; quarterly for executive risk owner and above. |
| `notes` | Optional | Key constraints, exclusions, or active exception IDs. |

## Keeping it current

- **Discovery feeds the register:** reconcile quarterly against SSO/IdP app grants, API-key billing, egress logs, cloud accounts, Git repositories (`AGENTS.md`, `SKILL.md`, MCP configs) and SaaS tenant admin settings.
- **Measure coverage honestly:** track registered-vs-discovered systems as `KRI-01` and newly discovered unregistered tools as `KRI-02` in the [KRI library](../board/kri-library.md).
- **Retire, do not delete:** move withdrawn systems to `Retired` once Gate 5 decommissioning ([INV-04](../framework/control-catalogue.md#inv-04)) is complete so audit history stays intact.
