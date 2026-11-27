# Reference Policy Enforcement Layer (OPA / Rego v1)
# Enforces controls outside the model:
#   IAM-01  Distinct non-human identity for every agent
#   IAM-02  Audience-bound tokens; no token passthrough
#   SUP-02  Verified MCP tool-definition hash (rug-pull protection)
#   ACT-01  Human approval for consequential actions at tier 2
#   ACT-02  Tool allow-list enforced outside the model
#   ACT-04  Egress allow-list and SSRF private/link-local blocking
#   ACT-06  Hard spend, token and step limits

package ai.governance.agent

import rego.v1

default allow := false

allow if {
	count(deny) == 0
}

# IAM-01: agent must run under a distinct non-human identity
deny contains msg if {
	input.agent.identity_type != "non_human"
	msg := "IAM-01: agent must run under a distinct non-human identity, not a user or shared account"
}

# IAM-02: audience-bound token required; reject passthrough tokens
deny contains msg if {
	input.tool.remote == true
	not input.auth.audience_match
	msg := sprintf("IAM-02: access token audience does not match target MCP server '%s'", [input.tool.server])
}

deny contains msg if {
	input.auth.token_passthrough == true
	msg := "IAM-02: token passthrough to upstream services is prohibited"
}

# SUP-02: tool definition hash must match the approved fingerprint
deny contains msg if {
	expected := data.approved_tool_hashes[input.tool.server][input.tool.name]
	input.tool.definition_sha256 != expected
	msg := sprintf("SUP-02: tool '%s/%s' definition hash changed since review (possible rug pull)", [input.tool.server, input.tool.name])
}

deny contains msg if {
	not data.approved_tool_hashes[input.tool.server][input.tool.name]
	msg := sprintf("SUP-01/SUP-02: tool '%s/%s' is not in the approved tool registry", [input.tool.server, input.tool.name])
}

# ACT-02: tool must be explicitly allow-listed for this agent
deny contains msg if {
	allowed_tools := object.get(data.agent_allowlists, input.agent.id, [])
	not input.tool.name in allowed_tools
	msg := sprintf("ACT-02: tool '%s' is not allow-listed for agent '%s'", [input.tool.name, input.agent.id])
}

# ACT-01: consequential actions require explicit human approval at tier <= 2
deny contains msg if {
	input.tool.consequential == true
	input.agent.autonomy_tier < 2
	msg := sprintf("ACT-01: tier %d agent cannot invoke consequential tool '%s'", [input.agent.autonomy_tier, input.tool.name])
}

deny contains msg if {
	input.tool.consequential == true
	input.agent.autonomy_tier == 2
	not valid_human_approval
	msg := sprintf("ACT-01: consequential tool '%s' requires explicit human approval bound to exact parameters", [input.tool.name])
}

valid_human_approval if {
	input.approval.granted == true
	input.approval.parameters_sha256 == input.tool.parameters_sha256
}

# ACT-04: egress allow-list and SSRF blocking (private / link-local ranges)
private_cidrs := [
	"10.0.0.0/8",
	"172.16.0.0/12",
	"192.168.0.0/16",
	"127.0.0.0/8",
	"169.254.0.0/16",
	"::1/128",
	"fc00::/7",
	"fe80::/10",
]

deny contains msg if {
	host := input.egress.host
	host != ""
	allowed_hosts := object.get(data.egress_allowlists, input.agent.id, [])
	not host in allowed_hosts
	msg := sprintf("ACT-04: outbound destination '%s' is not on the egress allow-list", [host])
}

deny contains msg if {
	ip := input.egress.resolved_ip
	ip != ""
	some cidr in private_cidrs
	net.cidr_contains(cidr, ip)
	msg := sprintf("ACT-04: outbound IP '%s' falls in blocked private/link-local range %s", [ip, cidr])
}

# ACT-06: hard resource and spend caps
deny contains msg if {
	limits := data.agent_limits[input.agent.id]
	input.usage.session_spend_usd > limits.max_spend_usd
	msg := sprintf("ACT-06: session spend %.2f exceeds cap %.2f", [input.usage.session_spend_usd, limits.max_spend_usd])
}

deny contains msg if {
	limits := data.agent_limits[input.agent.id]
	input.usage.tool_calls > limits.max_tool_calls
	msg := sprintf("ACT-06: tool call count %d exceeds cap %d", [input.usage.tool_calls, limits.max_tool_calls])
}
