# OPA reference policy enforcement layer

A starter [Open Policy Agent](https://www.openpolicyagent.org/) policy (`agent_policy.rego`) showing how to enforce agent controls **outside the model** ([ACT-02](../../framework/control-catalogue.md#act-02)).

## Controls enforced

- **[IAM-01](../../framework/control-catalogue.md#iam-01):** rejects requests where the agent runs under a human or shared credential.
- **[IAM-02](../../framework/control-catalogue.md#iam-02):** requires audience-bound tokens on remote MCP servers and blocks token passthrough.
- **[SUP-02](../../framework/control-catalogue.md#sup-02):** rejects any tool call whose tool-definition SHA-256 differs from the approved lockfile (see [MCP fingerprinting](../mcp-fingerprint/README.md)).
- **[ACT-01](../../framework/control-catalogue.md#act-01) & [ACT-02](../../framework/control-catalogue.md#act-02):** enforces per-agent tool allow-lists and requires human approval cryptographically bound to exact parameters for consequential actions at tier 2.
- **[ACT-04](../../framework/control-catalogue.md#act-04):** enforces egress host allow-lists and blocks private/link-local IP ranges (SSRF protection per [MCP policy §3.7](../../policies/mcp-and-agent-supply-chain-policy.md#37-runtime-controls)).
- **[ACT-06](../../framework/control-catalogue.md#act-06):** halts execution when session spend or tool-call budgets are exceeded.

## Running the tests

```bash
opa test examples/opa/ -v
```
