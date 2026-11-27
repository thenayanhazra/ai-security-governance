package ai.governance.agent_test

import rego.v1

import data.ai.governance.agent

mock_data := {
	"approved_tool_hashes": {
		"refunds-mcp": {
			"issue_refund": "sha256:abc123",
			"get_order": "sha256:def456",
		},
	},
	"agent_allowlists": {
		"AI-004": ["get_order", "issue_refund"],
	},
	"egress_allowlists": {
		"AI-004": ["api.payments.internal"],
	},
	"agent_limits": {
		"AI-004": {"max_spend_usd": 5.0, "max_tool_calls": 20},
	},
}

base_input := {
	"agent": {"id": "AI-004", "autonomy_tier": 2, "identity_type": "non_human"},
	"auth": {"audience_match": true, "token_passthrough": false},
	"tool": {
		"server": "refunds-mcp",
		"name": "issue_refund",
		"remote": true,
		"consequential": true,
		"definition_sha256": "sha256:abc123",
		"parameters_sha256": "sha256:params1",
	},
	"approval": {"granted": true, "parameters_sha256": "sha256:params1"},
	"egress": {"host": "api.payments.internal", "resolved_ip": "198.51.100.10"},
	"usage": {"session_spend_usd": 1.25, "tool_calls": 4},
}

test_allow_valid_tier2_approved_call if {
	agent.allow with input as base_input with data as mock_data
}

test_deny_rug_pull_changed_hash if {
	bad := json.patch(base_input, [{"op": "replace", "path": "/tool/definition_sha256", "value": "sha256:tampered"}])
	not agent.allow with input as bad with data as mock_data
}

test_deny_missing_approval_parameters_binding if {
	bad := json.patch(base_input, [{"op": "replace", "path": "/approval/parameters_sha256", "value": "sha256:other"}])
	not agent.allow with input as bad with data as mock_data
}

test_deny_ssrf_link_local if {
	bad := json.patch(base_input, [{"op": "replace", "path": "/egress/resolved_ip", "value": "169.254.169.254"}])
	not agent.allow with input as bad with data as mock_data
}

test_deny_spend_cap_exceeded if {
	bad := json.patch(base_input, [{"op": "replace", "path": "/usage/session_spend_usd", "value": 9.99}])
	not agent.allow with input as bad with data as mock_data
}

test_deny_token_passthrough if {
	bad := json.patch(base_input, [{"op": "replace", "path": "/auth/token_passthrough", "value": true}])
	not agent.allow with input as bad with data as mock_data
}
