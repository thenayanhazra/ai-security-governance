# MCP tool-definition fingerprinting starter

A zero-dependency Python CLI (`fingerprint_mcp.py`) implementing **[SUP-02](../../framework/control-catalogue.md#sup-02)** (*Version pinning and tool-definition change detection*) and measuring **KRI-06** (*Unreviewed tool changes*).

## Why it matters

MCP servers expose tool names, descriptions, input schemas and annotations that the model reads as instructions. A server that passes intake review can silently edit a tool description later ("rug pull", `AML.T0109`) to inject hidden instructions.

## Usage

1. Export the server's `tools/list` JSON response during intake review and generate a lockfile:

```bash
python examples/mcp-fingerprint/fingerprint_mcp.py lock tools.json \
  --server refunds-mcp \
  -o mcp-tools.lock.json
```

2. Verify the server's live `tools/list` output in CI or before loading tools at runtime:

```bash
python examples/mcp-fingerprint/fingerprint_mcp.py check tools.json \
  --lock mcp-tools.lock.json
```

Any added, removed, duplicated or modified tool description or schema exits non-zero and prints the exact tool name and SHA-256 mismatch. The resulting hashes also feed directly into `data.approved_tool_hashes` in the [OPA starter policy](../opa/agent_policy.rego).
