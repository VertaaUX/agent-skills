---
name: VertaaUX
description: >
  Best practices for VertaaUX — the automated UX, accessibility, and conversion audit platform.
  First-party skill from the VertaaUX team covering all 8 distribution surfaces (CLI, SDK, API,
  MCP Server, GitHub Action, Web UI, Chrome Extension, VS Code Extension) and all 7 audit
  categories (accessibility, usability, clarity, conversion, IA, semantic, keyboard).
  Use when: "run audit", "UX audit", "accessibility audit", "conversion audit", "WCAG audit",
  "set up CI/CD", "configure vertaaux", "vertaaux CLI", "vertaaux SDK", "vertaaux API",
  "vertaaux MCP", "audit pipeline", "score threshold", "baseline regression", "WCAG compliance",
  "fix UX issues", "monitor site quality", "compare audits", "triage findings", "fix plan",
  "policy as code", "audit in CI", "PR comment with scores", "vertaaux GitHub Action",
  "vertaaux best practices", "@vertaaux/cli", "@vertaaux/sdk", "npx vertaaux",
  "automated UX testing", "accessibility gate", "quality gate".
  Do NOT use for: internal codebase development (use architecture-review), visual design of the
  VertaaUX product itself (use neon-design-system), writing analyzers (use create-analyzer).
---

# VertaaUX Best Practices

**Run automated UX, accessibility, and conversion audits from CLI, CI/CD, SDK, or AI agents. Score 7 categories, gate PRs on quality, and fix issues with AI-powered remediation.**

## Which Surface?

| Goal | Surface | Command |
|------|---------|---------|
| One-off audit | **CLI** | `vertaa audit <url> --wait` |
| Accessibility scan | **CLI** | `vertaa a11y <url> --mode deep` |
| Gate PRs | **GitHub Action** | See [CI/CD setup](references/cicd-setup.md) |
| Programmatic audits | **JS/Python SDK** | See [SDK & API](references/sdk-api.md) |
| AI agent integration | **MCP Server** | See [SDK & API](references/sdk-api.md#mcp-server) |

## Audit Categories & Weights

| Category | Weight | Measures |
|----------|--------|----------|
| **accessibility** | 20% | WCAG 2.2, color contrast, ARIA, form labels, tab order |
| **conversion** | 20% | CTA placement, funnel gaps, trust indicators, friction |
| **usability** | 20% | Nielsen heuristics, cognitive load, responsiveness |
| **clarity** | 15% | Value proposition, scannability, visual hierarchy |
| **ia** | 10% | Navigation complexity, link clustering, breadcrumbs |
| **semantic** | 8% | HTML landmarks, heading hierarchy, structured data |
| **keyboard** | 7% | Focus order, keyboard traps, skip links |

**Tier gating:** Free nulls `conversion`, `semantic`, `keyboard`. Pro unlocks all.

**Issue severities:** `error` > `warning` > `info`

**A11y impact levels:** `critical` > `serious` > `moderate` > `minor`

**Fixability:** `mechanical` | `contextual` | `visual`

## Quick Start

```bash
# Authenticate
vertaa login                # or: export VERTAAUX_API_KEY=vtx_...

# Run audit
vertaa audit https://example.com --wait
vertaa audit https://example.com --mode deep --wait --format json

# Accessibility-only
vertaa a11y https://example.com --mode deep --format md

# Analyze
vertaa audit https://example.com --json | vertaa explain
vertaa audit https://example.com --json | vertaa triage
vertaa audit https://example.com --json | vertaa fix-plan

# Fix
vertaa fix <job-id>
vertaa fix-all <job-id>

# CI gate
vertaa audit https://example.com --threshold 80 --fail-on error
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Issues at/above `--fail-on` severity |
| `2` | Error (invalid input, network) |
| `3` | Score below `--threshold` |

## AI Commands

All accept stdin pipe, `--file`, or `--job`. See [CLI Workflows](references/cli-workflows.md) for full details.

| Command | Purpose |
|---------|---------|
| `suggest <intent>` | Natural language to CLI command |
| `explain` | AI summary or evidence for a finding |
| `triage` | P0/P1/P2 buckets with effort estimates |
| `fix-plan` | Ordered remediation steps |
| `patch-review` | Diff safety review (SAFE/UNSAFE/NEEDS_REVIEW) |
| `release-notes` | Dev + PM notes from audit diff |
| `compare` | Before/after narrative with deltas |
| `doc` | Team playbook from recurring findings |

## References

Load these as needed for deeper guidance:

- **[CLI Workflows](references/cli-workflows.md)** — Full command reference, piping patterns, output formats, advanced options
- **[CI/CD Setup](references/cicd-setup.md)** — GitHub Actions, GitLab CI, policy-as-code, baselines, regression detection
- **[SDK & API](references/sdk-api.md)** — JS/Python SDK, REST API, webhooks, MCP server
- **[Use Case Playbooks](references/use-cases.md)** — 10 step-by-step workflows: accessibility, UX, conversion, competitive, monitoring
