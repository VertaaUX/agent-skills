<div align="center">

<img src="banner.svg" alt="VERTAAUX" width="800"/>

**Automated UX, accessibility, and conversion audits for AI coding agents.**

</div>

---

## Install

```bash
npx skills add VertaaUX/agent-skills
```

## Available Skills

### VertaaUX

Best practices for the VertaaUX automated audit platform. Covers CLI, SDK, API, GitHub Action, MCP Server, and more.

**What your agent learns:**

- Run 7-category UX audits via CLI, SDK, or API
- Set up CI/CD quality gates with score thresholds and regression detection
- Deep WCAG accessibility scans (axe-core + AccessLint + custom analyzers)
- AI-powered triage, fix plans, and patch generation
- Policy-as-code for team-wide quality standards

**Audit categories:** Accessibility (20%), Conversion (20%), Usability (20%), Clarity (15%), IA (10%), Semantic (8%), Keyboard (7%)

## Quick Start

```bash
npm install -g @vertaaux/cli
vertaa login
vertaa audit https://example.com --wait
vertaa a11y https://example.com --mode deep
```

## Compatibility

Works with Claude Code, Cursor, Codex, GitHub Copilot, Gemini CLI, Windsurf, Cline, Roo, and more.
