---
name: vertaaux
description: Run and operationalize VertaaUX UX, accessibility, and conversion audits across CLI, CI/CD, SDK, API, and MCP. Use when the user needs to audit a URL, investigate WCAG issues, set quality gates, compare audit runs, or generate remediation plans from VertaaUX results.
license: MIT
metadata:
  author: vertaaux
  version: "1.2.0"
---

# VertaaUX

Use VertaaUX to audit live experiences, explain findings, and turn results into CI gates or fix plans.

## When to Use

- Run a full UX audit for a live URL
- Run or interpret accessibility and WCAG-focused scans
- Set up VertaaUX in CI/CD or PR quality gates
- Compare audit runs, baselines, or regressions
- Generate triage, fix plans, or patch reviews from audit output
- Integrate VertaaUX through the SDK, API, or MCP server

## Fast Path

| Goal | Surface | Command |
|------|---------|---------|
| Full audit | CLI | `vertaa audit <url> --wait` |
| Accessibility scan | CLI | `vertaa a11y <url> --mode deep` |
| PR or CI gate | GitHub Action / CI | See [CI/CD setup](references/cicd-setup.md) |
| Programmatic workflow | JS or Python SDK | See [SDK & API](references/sdk-api.md) |
| Agent integration | MCP Server | See [SDK & API](references/sdk-api.md#mcp-server) |

## Quick Example

```bash
# Authenticate once
vertaa login

# Run an audit and inspect the result
vertaa audit https://example.com --wait --format json > audit.json
cat audit.json | vertaa explain
cat audit.json | vertaa triage
```

## Recommended Workflow

1. Pick the lightest surface that fits the task.
   Use the CLI for one-off audits, CI for gates, and SDK/API or MCP only when the workflow needs automation.
2. Authenticate before deeper work.
   Use `vertaa login` or set `VERTAAUX_API_KEY` before running commands that need cloud access.
3. Run the smallest audit that answers the question.
   Start with `vertaa audit <url> --wait` for broad UX checks or `vertaa a11y <url> --mode deep` for accessibility-specific work.
4. Convert results into action.
   Pipe results into `vertaa explain`, `vertaa triage`, `vertaa fix-plan`, `vertaa compare`, or `vertaa patch-review` depending on whether the user needs diagnosis, prioritization, or remediation.
5. Load deeper references only when the task actually needs them.
   Use the matching reference below instead of inlining every edge case into the main skill.

## Audit Model

| Category | Weight | Focus |
|----------|--------|-------|
| `accessibility` | 20% | WCAG 2.2, ARIA, contrast, labels, focus |
| `conversion` | 20% | CTA strength, funnel gaps, trust, friction |
| `usability` | 20% | Heuristics, responsiveness, cognitive load |
| `clarity` | 15% | Messaging, hierarchy, scannability |
| `ia` | 10% | Navigation, grouping, findability |
| `semantic` | 8% | Landmarks, headings, structured markup |
| `keyboard` | 7% | Focus order, traps, skip links |

Notes:

- Free tier nulls `conversion`, `semantic`, and `keyboard`; Pro unlocks all categories.
- Findings are ordered by severity: `error`, `warning`, `info`.
- Accessibility impact levels are `critical`, `serious`, `moderate`, `minor`.
- Severity and accessibility impact are different fields. Commands such as `--fail-on error` use severity, while `fail-on-critical` style CI options refer to accessibility impact.
- Fixability values are `mechanical`, `contextual`, and `visual`.

## AI Follow-up Commands

All of these accept stdin, `--file`, or `--job`. See [CLI Workflows](references/cli-workflows.md) for complete usage.

| Command | Purpose |
|---------|---------|
| `suggest <intent>` | Natural language to CLI command |
| `explain` | Explain findings or surface evidence |
| `triage` | Bucket work into priorities with effort |
| `fix-plan` | Build an ordered remediation plan |
| `patch-review` | Review a diff against audit findings |
| `compare` | Describe before/after deltas |
| `release-notes` | Turn audit diffs into dev or PM notes |
| `doc` | Build a repeatable team playbook |

Comparison notes:

- Use `vertaa compare --before <file> --after <file>` for saved audit outputs.
- Use `vertaa compare <url-a> <url-b>` when comparing live URLs directly.

## References

Load only the reference that matches the active task:

- [CLI Workflows](references/cli-workflows.md) for command syntax, formats, piping, and advanced options
- [CI/CD Setup](references/cicd-setup.md) for GitHub Actions, baselines, thresholds, and regression gates
- [SDK & API](references/sdk-api.md) for JS/Python SDK usage, REST API calls, webhooks, and MCP setup
- [Use Case Playbooks](references/use-cases.md) for step-by-step workflows such as accessibility audits, monitoring, competitive analysis, and remediation
