# MCP server and agent component policy

| | |
|---|---|
| **Policy owner** | [Executive AI risk owner] |
| **Approved by** | [AI risk forum] |
| **Effective** | [Date] |
| **Review** | Every 12 months, or sooner if the MCP specification or a referenced framework changes |
| **Related** | [AI and Agent Risk Framework](../framework/ai-agent-risk-framework.md), [control catalogue](../framework/control-catalogue.md) |

## 1. Purpose

AI agents extend what they can do by loading components written by other people: MCP servers, skills, plugins and instruction files. Each one can read data, take actions and, through its descriptions and outputs, influence what the agent decides to do next. A compromised or careless component can redirect an agent, leak data or act with the agent's authority.

This policy sets the conditions under which those components may be used.

## 2. Scope

This policy applies to:

- **MCP servers:** local or remote, internal or third-party, whether connected to an agent built here or to an AI product used here (for example, an IDE assistant or a desktop AI client).
- **Skills, plugins and extensions** that add tools or instructions to an agent.
- **Instruction files** that agents load as guidance, including SKILL.md, AGENTS.md, IDE rule files and MCP client configuration.

It applies to all employees, contractors and systems. Personal experimentation on corporate devices or with corporate data is in scope.

## 3. Policy statements

### 3.1 Approved sources only

1. Components **must** be installed only from the approved component registry. A component not in the registry may not be connected to any agent that has access to corporate data or systems.
2. Requests to add a component go through intake review (section 4). Approval applies to a specific version, not to the component in general.
3. Components that are no longer maintained, or whose maintainer cannot be identified, **must not** be approved for tier 2 or tier 3 agents.

### 3.2 Pinning and change control

1. Approved components **must** be pinned to the reviewed version or content hash.
2. The tool definitions an MCP server exposes (names, descriptions and input schemas) **must** be recorded at approval. If they change, the component **must** be blocked automatically until it is reviewed again. Description changes are treated as code changes, because the model reads them as instructions.
3. Updates follow the same intake review, scaled to the size of the change.

### 3.3 Authentication and authorisation for remote MCP servers

Remote MCP servers built or operated here **must** meet the security requirements of the MCP authorization specification (version 2026-07-28 at the time of writing). In particular:

1. Servers **must** accept only access tokens issued specifically for them, and reject any token whose audience does not include them.
2. Servers **must not** pass a client's token through to an upstream API. Where a server calls another service, it uses a separate token issued for that service.
3. Clients **must** request tokens with the `resource` parameter (RFC 8707) so tokens are bound to the intended server.
4. Clients **must** use PKCE with the `S256` method, and refuse to proceed if the authorization server does not advertise PKCE support.
5. All authorization endpoints **must** use HTTPS. Redirect URIs **must** be HTTPS or `localhost`, and must match the registered value exactly.
6. Proxy servers that use a static client ID with a third-party API **must** obtain the user's consent for each client before forwarding to the third party.
7. Scopes **must** follow least privilege: start with the minimum needed and step up only when a privileged operation is first attempted. Wildcard or all-access scopes are not permitted.

Third-party remote servers are assessed against the same requirements during intake. A server that cannot meet them may be approved only for tier 0 or tier 1 use with non-sensitive data.

### 3.4 Local MCP servers

1. Local servers **must** run with the least privilege practical: in a container or sandbox, with file-system access limited to the directories they need and network access limited to an allow-list.
2. Before a local server is configured, the user **must** be shown the exact command that will run, in full.
3. Local servers **should** use the `stdio` transport. If they use HTTP, they **must** require an authorization token or use a restricted inter-process channel, so other processes on the machine cannot reach them.

### 3.5 Credentials and secrets

1. Secrets **must not** appear in MCP configuration files, instruction files, tool descriptions or prompts. They are supplied at run time by the approved secrets broker.
2. Tokens **must** be short-lived and stored securely. Refresh tokens for public clients **must** be rotated.

### 3.6 Instruction files

1. Instruction files **must** be scanned before merge or installation for hidden Unicode (bidirectional controls, zero-width characters, tag characters), instruction-override patterns, references to credential locations and data-exfiltration sinks such as image URLs with data-carrying parameters.
2. Instruction files from outside the organisation are third-party components and follow section 3.1.

### 3.7 Runtime controls

1. Tool calls from agents **must** pass through a policy enforcement layer that applies an allow-list of tools, parameters and destinations. Approval of a component does not grant it unlimited use.
2. Every tool call **must** be logged with the agent identity, the component and version, the parameters and the result status.
3. Egress from MCP servers and from MCP clients deployed on servers **must** be limited to approved destinations, with private and link-local address ranges blocked to prevent server-side request forgery.

## 4. Intake review

Every new component, and every update, is reviewed before approval. The depth of review depends on the highest autonomy tier of any agent that will use it.

| Check | Tier 0–1 | Tier 2–3 |
|---|---|---|
| Provenance: publisher identity, repository, licence, maintenance activity | Required | Required |
| Permissions: tools exposed, data and systems reachable, scopes requested | Required | Required |
| Static scan of instruction files and tool definitions | Required | Required |
| Secrets and dependency scan | Required | Required |
| Adversarial test: tool poisoning, indirect injection through results, exfiltration, confused deputy | Recommended | Required |
| Authorization review against section 3.3 (remote servers) | Required if sensitive data | Required |
| Security owner sign-off | Team lead | AI risk forum |

Open-source tooling that supports this review:

- [agentlint](https://github.com/thenayanhazra/agentlint) for static scanning of instruction files and MCP configuration.
- [MCP Adversarial Harness](https://github.com/thenayanhazra/mcp-adversarial-harness) for adversarial testing of MCP servers.

## 5. Roles

| Role | Responsibility |
|---|---|
| Executive AI risk owner | Owns this policy and approves exceptions for tier 2 and 3 |
| AI risk forum | Approves components for tier 2 and 3 agents |
| Security | Runs intake testing, maintains detection for changed tool definitions, investigates incidents |
| Platform engineering | Operates the component registry, policy enforcement layer and secrets broker |
| Component requester | Provides the information intake needs and keeps the inventory entry current |
| All staff | Use only approved components; report suspicious behaviour |

## 6. Exceptions

Exceptions are requested through the AI risk forum with a business justification, compensating controls and an expiry date of no more than 90 days. Exceptions for tier 3 agents need the executive AI risk owner's approval. All exceptions are recorded and reported in the quarterly AI risk report.

## 7. Monitoring and enforcement

Compliance is measured through the [key risk indicators](../board/kri-library.md), in particular inventory coverage (KRI-01), unregistered AI found (KRI-02) and unreviewed tool changes (KRI-06). Unapproved components found in use are disconnected, and the owning team is notified. Repeated or deliberate breaches are handled under the disciplinary policy.

## 8. Definitions

| Term | Meaning |
|---|---|
| MCP | Model Context Protocol, an open protocol that lets AI applications connect to tools and data sources |
| MCP server | A program that exposes tools, resources or prompts to an AI application over MCP |
| Tool definition | The name, description and input schema an MCP server publishes for each tool |
| Tool poisoning | Hidden instructions placed in a tool definition so that the model follows them |
| Rug pull | A component that changes its behaviour or definitions after it has been approved |
| Token passthrough | An MCP server forwarding a token it received to another service, instead of obtaining its own |
| Autonomy tier | The classification of an agent by what it can do without human approval, defined in the risk framework |

## 9. References

- Model Context Protocol specification 2026-07-28: [Authorization security considerations](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations) and [Security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- OWASP Top 10 for Agentic Applications 2026: ASI04 Agentic Supply Chain Vulnerabilities
- MITRE ATLAS v2026.10: AML.T0010.005 (Supply Chain Compromise: AI Agent Tool), AML.T0109 (AI Supply Chain Rug Pull), AML.T0110 (AI Agent Tool Poisoning)
