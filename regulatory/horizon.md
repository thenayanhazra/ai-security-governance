# Regulatory and standards horizon

**Status as of 12 November 2026.** This page records which version of each framework the repository maps to, and the dates that matter for planning. It summarises public sources and is not legal advice; confirm obligations with counsel.

## Versions this repository maps to

| Framework | Version used | Notes |
|---|---|---|
| NIST AI Risk Management Framework | AI RMF 1.0 (NIST AI 100-1) | NIST has stated that 1.0 is being revised under the White House AI Action Plan. No release date announced. |
| ISO/IEC 42001 | 2023 edition, Annex A | 38 reference controls across 9 objectives (A.2 to A.10). |
| EU AI Act | Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744 | The amending "Digital Omnibus on AI" entered into force on 27 July 2026. |
| OWASP Top 10 for LLM Applications | 2026 edition, published August 2026 | Re-ordered from 2025. Excessive Agency rose to LLM03; System Prompt Leakage was broadened and renamed Hidden Context Exposure (LLM08). Some OWASP pages still show the 2025 list. |
| OWASP Top 10 for Agentic Applications | 2026 edition, published December 2025 | First edition. ASI01 to ASI10. |
| MITRE ATLAS | v2026.10 | Several technique IDs that appear in older guidance have since been retired or renamed. Every ATLAS ID in this repository is checked against MITRE's published data in CI. |
| Model Context Protocol | Specification 2026-07-28 | Authorization and security best practices referenced in the [supply-chain policy](../policies/mcp-and-agent-supply-chain-policy.md). |

## EU AI Act: key dates after the Digital Omnibus

| Date | What applies | Changed by the Omnibus? |
|---|---|---|
| 2 Feb 2025 | Prohibited practices (Art. 5) and AI literacy (Art. 4) | Art. 4 reworded: providers and deployers must take measures to support AI literacy |
| 2 Aug 2025 | General-purpose AI model obligations; governance; penalties | No |
| 2 Aug 2026 | General application, including transparency obligations (Art. 50) | No |
| 2 Dec 2026 | Two new prohibitions added by the Omnibus (non-consensual intimate imagery; child sexual abuse material). Deadline for machine-readable marking (Art. 50(2)) for generative systems already on the market before 2 Aug 2026 | Yes, new |
| 2 Aug 2027 | General-purpose AI models placed on the market before 2 Aug 2025 must comply | No |
| 2 Dec 2027 | High-risk obligations for stand-alone systems listed in Annex III | Yes, deferred from 2 Aug 2026 |
| 2 Aug 2028 | High-risk obligations for AI in products covered by Annex I | Yes, deferred from 2 Aug 2027 |

The deferral moves enforcement, not the requirements. Risk management (Art. 9), record-keeping (Art. 12), human oversight (Art. 14) and accuracy, robustness and cybersecurity (Art. 15) still apply to high-risk systems from those dates, and they take time to evidence.

## Other developments to watch

| Development | Status | Relevance |
|---|---|---|
| NIST Cyber AI Profile (NIST IR 8596) | Preliminary draft released December 2025; comment period closed 30 January 2026 | Applies the NIST Cybersecurity Framework 2.0 to AI. Expect to map controls to it once finalised. |
| NIST AI Agent Standards Initiative | Launched February 2026 by NIST's Center for AI Standards and Innovation | Likely source of agent-specific guidance. |
| NIST AI RMF revision | Announced; no date | The crosswalk will need updating when it is published. |

## How this page is maintained

When a framework publishes a new version: update `data/references.yaml`, review the affected mappings in `data/controls.yaml`, run `python tools/build.py`, and update this page. The CI check warns when MITRE publishes a new ATLAS release so mappings can be reviewed.

## Sources

- European Commission and EUR-Lex: Regulation (EU) 2024/1689 and Regulation (EU) 2026/1744
- NIST: [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) and [AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)
- NIST CSRC: [Preliminary draft Cyber AI Profile](https://csrc.nist.gov/News/2025/nist-releases-prelim-draft-cyber-ai-profile)
- OWASP GenAI Security Project: [Top 10 for LLM Applications 2026 announcement](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)
- MITRE: [ATLAS data](https://github.com/mitre-atlas/atlas-data)
- Model Context Protocol: [Specification 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization/security-considerations)
