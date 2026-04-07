<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="banner-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="banner-light.svg" />
  <img src="banner-light.svg" alt="VERTAAUX" width="800" />
</picture>

[![Release](https://img.shields.io/github/v/release/VertaaUX/agent-skills?display_name=tag)](https://github.com/VertaaUX/agent-skills/releases)
[![Repo Checks](https://img.shields.io/github/actions/workflow/status/VertaaUX/agent-skills/repo-hygiene.yml?branch=main&label=repo%20checks)](https://github.com/VertaaUX/agent-skills/actions/workflows/repo-hygiene.yml)
[![License](https://img.shields.io/github/license/VertaaUX/agent-skills)](LICENSE)
[![npm](https://img.shields.io/npm/v/%40vertaaux%2Fcli?label=%40vertaaux%2Fcli)](https://www.npmjs.com/package/@vertaaux/cli)
[![Format](https://img.shields.io/badge/format-Agent%20Skills-0f172a)](https://agentskills.io/)

**Production-oriented agent skills for VertaaUX accessibility, UX, and conversion audits.**

</div>

This repository packages VertaaUX guidance in the open [Agent Skills](https://agentskills.io/) format so coding agents can run audits, interpret findings, and turn results into CI gates or remediation plans without inventing unsupported commands.

## Quick Start

Install the published skills package:

```bash
npx skills add VertaaUX/agent-skills
```

Preview the packaged skills before installing:

```bash
npx skills add VertaaUX/agent-skills --list
```

Install only the VertaaUX skill:

```bash
npx skills add VertaaUX/agent-skills --skill vertaaux
```

Run a minimal VertaaUX workflow:

```bash
npm install -g @vertaaux/cli
vertaa login
vertaa audit https://example.com --profile quick-ux --wait --format json > audit.json
cat audit.json | vertaa triage
```

## What This Repo Gives You

- A production-ready `vertaaux` skill for URL audits, WCAG investigations, CI gates, and agent-driven remediation workflows
- Reference documents for audit profiles, CLI workflows, CI/CD setup, SDK/API usage, and reusable playbooks
- Guardrails that keep agents aligned with real VertaaUX surfaces instead of hallucinated flags or parameters
- Composition contracts for handing off VertaaUX work into adjacent review or architecture skills

## Available Skill

### `vertaaux`

Run and operationalize VertaaUX audits across CLI, CI/CD, SDK, API, and MCP.

Use it when the user needs to:

- audit a live URL for UX, accessibility, or conversion issues
- investigate WCAG findings or accessibility regressions
- set up CI or PR quality gates with thresholds and baselines
- compare audit runs and explain score deltas
- generate triage, fix plans, patch reviews, or team playbooks from audit output

## What It Covers

- **Audit profiles**: built-in and custom profile definitions, selection decision tree, and category filtering
- **Task recipes**: deterministic step sequences for accessibility audits, monitoring, remediation, and competitive review
- **Verification and drift control**: guardrails that prevent the agent from inventing flags, parameters, or commands the CLI/API doesn't actually expose
- **Skill composition contracts**: explicit input/output/handoff conventions so `vertaaux` can chain into `a11y-review`, `create-analyzer`, and `architecture-review` without guesswork
- **CLI workflows** for one-off audits and AI follow-up commands
- **CI/CD setup** for score thresholds, baselines, and regression detection
- **SDK, API, and MCP** integration for automated workflows and agent-driven tooling

## Typical Outcomes

- **Fast audit selection** with documented profiles such as `quick-ux`, `wcag-aa`, and `ci-gate`
- **Deterministic follow-up flows** for explanation, triage, comparison, and fix planning
- **Operational CI guidance** for score thresholds, baselines, and regression detection
- **Programmatic integration patterns** for SDK, API, webhooks, and MCP-driven agents

## Repository Layout

- `skills/vertaaux/SKILL.md` - Main skill instructions and routing guidance
- `skills/vertaaux/references/audit-profiles.md` - Built-in profiles, custom profile schema, and profile selection guidance
- `skills/vertaaux/references/cli-workflows.md` - Command reference and piping patterns
- `skills/vertaaux/references/cicd-setup.md` - CI/CD and GitHub Actions examples
- `skills/vertaaux/references/sdk-api.md` - SDK, API, webhook, and MCP details
- `skills/vertaaux/references/use-cases.md` - Task recipes and step-by-step workflow playbooks
- `skills/vertaaux/references/skill-contracts.md` - Skill composition contracts for chaining `vertaaux` with `a11y-review`, `create-analyzer`, and `architecture-review`

## Compatibility

This repository is designed for tools that support the Agent Skills format.

Common hosts include:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/compatibility/compatibility-grid-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/compatibility/compatibility-grid-light.svg" />
  <img src="assets/compatibility/compatibility-grid-light.svg" alt="Compatibility hosts" width="100%" />
</picture>

Logos are sourced from a single upstream package and vendored locally. See [assets/compatibility/SOURCES.md](assets/compatibility/SOURCES.md).

If your environment can install Agent Skills from GitHub, this repository should fit directly into that workflow.

## Project Standards

- Changes should preserve documented VertaaUX behavior and avoid inventing unsupported CLI flags or API fields.
- Documentation updates should keep examples executable and relative links valid.
- Repo hygiene checks run in GitHub Actions on pull requests and pushes to `main`.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution expectations and [SECURITY.md](SECURITY.md) for vulnerability reporting guidance.

## License

MIT
