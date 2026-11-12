# Key risk indicators for AI and agents

Twelve indicators that show whether the [risk framework](../framework/ai-agent-risk-framework.md) is working. Each one is measurable from systems most organisations already run, and each links to the controls it tests.

The thresholds are starting points. Calibrate them to the organisation's risk appetite, its size and how many agents it runs, then hold them steady so trends mean something.

| ID | Indicator | How it is measured | Green | Amber | Red | Controls |
|---|---|---|---|---|---|---|
| KRI-01 | Inventory coverage | Registered AI systems, agents and components with a named owner, as a share of all found by discovery | ≥ 98% | 90–98% | < 90% | [INV-01](../framework/control-catalogue.md#inv-01), [GOV-01](../framework/control-catalogue.md#gov-01) |
| KRI-02 | Unregistered AI found | New AI tools, MCP servers or agents found in use without registration, per quarter | ≤ 5 | 6–15 | > 15 | [INV-01](../framework/control-catalogue.md#inv-01), [SUP-01](../framework/control-catalogue.md#sup-01) |
| KRI-03 | Assessment currency | Tier 2 and 3 systems whose threat and impact assessment reflects their current tools, data and tier | 100% | 95–99% | < 95% | [INV-03](../framework/control-catalogue.md#inv-03) |
| KRI-04 | Prompt injection bypass rate | Median share of the standard attack corpus that succeeds against tier 2 and 3 agents | ≤ 5% | 5–15% | > 15% | [TST-01](../framework/control-catalogue.md#tst-01), [TST-02](../framework/control-catalogue.md#tst-02) |
| KRI-05 | Time to stop an agent | Longest time, in the latest exercise, to pause a tier 3 agent and revoke its credentials | ≤ 15 min | 15–60 min | > 60 min, or no exercise in 6 months | [OPS-02](../framework/control-catalogue.md#ops-02) |
| KRI-06 | Unreviewed tool changes | MCP tool definitions in use that changed since their last review | 0 | 1–2, each under 48 hours old | Any older than 48 hours | [SUP-02](../framework/control-catalogue.md#sup-02) |
| KRI-07 | Rubber-stamp rate | Human approvals given in under three seconds, as a share of all approvals | < 10% | 10–25% | > 25% | [HUM-02](../framework/control-catalogue.md#hum-02), [ACT-01](../framework/control-catalogue.md#act-01) |
| KRI-08 | Over-privileged agents | Agents holding scopes beyond their documented need at the last access review | < 5% | 5–15% | > 15% | [IAM-02](../framework/control-catalogue.md#iam-02) |
| KRI-09 | Agents without their own identity | Agents acting under a person's account or a shared account | 0 | 1–2, with approved exception | > 2, or any without exception | [IAM-01](../framework/control-catalogue.md#iam-01) |
| KRI-10 | Overdue AI security findings | Critical and high findings on AI systems past their remediation deadline | 0 | 1–3 | > 3 | [TST-01](../framework/control-catalogue.md#tst-01), [TST-03](../framework/control-catalogue.md#tst-03) |
| KRI-11 | AI security incidents | Incidents involving AI systems in the quarter, by severity | No severity 1 or 2 | One severity 2 | Any severity 1 | [OPS-03](../framework/control-catalogue.md#ops-03), [OPS-04](../framework/control-catalogue.md#ops-04) |
| KRI-12 | Training coverage | In-scope staff who completed role-based AI training in the last 12 months | ≥ 95% | 85–95% | < 85% | [GOV-04](../framework/control-catalogue.md#gov-04) |

## Notes on the harder ones

**KRI-04, bypass rate.** Use the same corpus every quarter so results are comparable, and add new techniques as a separate line until there is a baseline for them. Report the median across agents, and name any single agent above the red threshold. The [LLM Prompt Injection Fuzzer](https://github.com/thenayanhazra/llm-prompt-injection-fuzzer) produces this number per category.

**KRI-05, time to stop.** Measure from the decision to stop until the agent has stopped acting and its credentials no longer work, not until someone has opened a ticket. An exercise that has not happened counts as red.

**KRI-06, unreviewed tool changes.** MCP servers can change a tool's description after it has been approved. This indicator only works if tool definitions are fingerprinted at approval time; if they are not, report it as "not measurable" rather than zero.

**KRI-07, rubber-stamp rate.** Three seconds is roughly the time it takes to read one line. A high rate usually means approvals are requested too often, not that reviewers are careless. The fix is fewer, clearer approval requests.
