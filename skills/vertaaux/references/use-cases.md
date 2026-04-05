# Use Case Playbooks

Step-by-step guides for common VertaaUX workflows. Each playbook is self-contained.

## Table of Contents

- [Accessibility Audit](#accessibility-audit)
- [Full UX Audit](#full-ux-audit)
- [Conversion Audit](#conversion-audit)
- [Competitive Comparison](#competitive-comparison)
- [Site Monitoring](#site-monitoring)
- [PR Quality Gate](#pr-quality-gate)
- [Remediation Workflow](#remediation-workflow)
- [AI Agent Integration](#ai-agent-integration)
- [Multi-Page Site Audit](#multi-page-site-audit)
- [WCAG Compliance Report](#wcag-compliance-report)

---

## Accessibility Audit

**Goal:** Find and fix WCAG violations before they reach users.

Severity note:
- General issue severity uses `error`, `warning`, `info`.
- Accessibility findings also carry impact levels `critical`, `serious`, `moderate`, `minor`.
- In the examples below, "critical findings" means accessibility-impact `critical`, not a separate top-level severity enum.

### Quick scan (< 30s)

```bash
vertaa a11y https://example.com --format md
```

### Deep compliance check

```bash
# Deep mode uses axe-core + AccessLint + custom analyzers (keyboard, live regions, semantic)
vertaa a11y https://example.com --mode deep --format md > a11y-report.md

# Filter to only serious+ issues
vertaa a11y https://example.com --mode deep --min-impact serious

# CI gate: fail if accessibility score < 85 or > 3 accessibility-impact critical findings
vertaa a11y https://example.com --mode deep \
  --fail-on-score 85 \
  --fail-on-findings 3
```

### Understanding results

Each finding includes:
- **wcagCriteria** — e.g., `1.4.3` (color contrast), `2.1.1` (keyboard accessible)
- **fixability** — `mechanical` (automatable, like adding alt text), `contextual` (needs human judgment), `visual` (design decision)
- **structured_fix** — machine-actionable operation: `add-attribute`, `set-attribute`, `remove-element`
- **impact** — `critical`, `serious`, `moderate`, `minor` (a11y-specific; mapped to severity `error`/`warning`/`info` in audit results)

### Fix workflow

```bash
# Get AI-powered fix suggestions
vertaa a11y https://example.com --mode deep --format json | vertaa fix-plan

# Generate patches
vertaa fix <job-id>
vertaa fix-all <job-id>

# Verify fix works
vertaa verify
```

### Multi-engine dedup

VertaaUX deduplicates across engines using: `selector + wcagCriteria + ruleId` (all three must match). This prevents merging distinct violations that happen to share a selector.

---

## Full UX Audit

**Goal:** Comprehensive UX assessment across all 7 categories.

```bash
# Standard depth — good balance of speed and coverage
vertaa audit https://example.com --mode standard --wait

# Deep mode — most thorough, ~40s
vertaa audit https://example.com --mode deep --wait --format json > audit.json

# AI summary of findings
cat audit.json | vertaa explain --verbose

# Priority triage with effort estimates
cat audit.json | vertaa triage

# Structured remediation plan
cat audit.json | vertaa fix-plan --json
```

### Score interpretation

| Score | Rating | Action |
|-------|--------|--------|
| 90-100 | Excellent | Minor polish |
| 75-89 | Good | Address high-severity issues |
| 50-74 | Needs work | Prioritize critical + high issues |
| 0-49 | Poor | Major redesign needed |

### Category weights (overall score)

accessibility (20%) + conversion (20%) + usability (20%) + clarity (15%) + ia (10%) + semantic (8%) + keyboard (7%)

### Free vs Pro

Free tier receives scores for: usability, clarity, ia, accessibility. The categories `conversion`, `semantic`, `keyboard` are nulled (upgrade to Pro). Issue count is also limited on free tier.

---

## Conversion Audit

**Goal:** Identify CTA, funnel, and trust issues hurting conversions.

```bash
# Full audit (conversion is one of 7 categories, weight: 20%)
vertaa audit https://example.com/pricing --mode deep --wait --format json > audit.json

# Extract conversion-specific findings
cat audit.json | jq '.data.issues[] | select(.category == "conversion")'

# AI analysis of conversion issues
cat audit.json | vertaa explain

# Generate team playbook for conversion improvements
cat audit.json | vertaa doc --team "Growth"
```

**What conversion analysis checks:**
- CTA placement, visibility, and wording strength
- Funnel gaps and dead-end pages
- Trust indicators (testimonials, badges, social proof)
- Layout friction and cognitive overload
- Mobile vs desktop conversion paths
- Form complexity and abandonment signals

**Note:** Conversion scoring requires Pro tier.

---

## Competitive Comparison

**Goal:** Compare your site against a competitor.

### URL-to-URL comparison

```bash
# Compare two URLs directly
vertaa compare https://yoursite.com https://competitor.com

# With LLM-powered narrative
vertaa compare --before yoursite-audit.json --after competitor-audit.json
```

### Structured comparison workflow

```bash
# Audit both sites
vertaa audit https://yoursite.com --mode standard --wait --format json > ours.json
vertaa audit https://competitor.com --mode standard --wait --format json > theirs.json

# Generate comparison narrative with score deltas
vertaa compare --before ours.json --after theirs.json

# Generate release notes style comparison
vertaa diff --job-a $OUR_JOB --job-b $THEIR_JOB --json | vertaa release-notes
```

---

## Site Monitoring

**Goal:** Track UX quality over time, catch regressions.

### Baseline setup

```bash
# Run initial audit and create baseline
vertaa audit https://example.com --mode standard --wait --format json > initial.json
JOB_ID=$(cat initial.json | jq -r '.data.job_id')
vertaa baseline $JOB_ID

# Baseline saved to .vertaaux/baseline.json
```

### Check for regressions

```bash
# Run new audit and compare
vertaa audit https://example.com --mode standard --wait
vertaa diff

# In CI: fail on regression
vertaa audit https://example.com --wait --threshold 80 --fail-on error
```

### Webhook-based monitoring

```typescript
import { createVertaauxClient } from "@vertaaux/sdk";

const client = createVertaauxClient({ apiKey: "vtx_..." });

// Set up webhook for completed audits
await client.createWebhook({
  url: "https://your-app.com/webhook/vertaaux",
  events: ["audit.completed"],
});

// Trigger periodic audits via API
await client.createAudit({
  url: "https://example.com",
  mode: "standard",
});
```

---

## PR Quality Gate

**Goal:** Block PRs that degrade UX quality.

### GitHub Actions (recommended)

`fail-on-critical` below refers to accessibility-impact `critical`, not the general issue severity field.

```yaml
name: UX Quality Gate
on: [pull_request]

jobs:
  ux-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: vertaaux/action@v1
        with:
          url: ${{ env.PREVIEW_URL }}
          api-key: ${{ secrets.VERTAAUX_API_KEY }}
          mode: standard
          threshold: 80
          fail-on-critical: true
          fail-on-regression: true
          comment-on-pr: true
          baseline-file: .vertaaux/baseline.json

      # Update baseline on main merges
      - uses: vertaaux/action@v1
        if: github.ref == 'refs/heads/main'
        with:
          url: https://example.com
          api-key: ${{ secrets.VERTAAUX_API_KEY }}
          update-baseline: true
```

### CLI-based gate

```bash
# Simple threshold
vertaa audit $PREVIEW_URL --wait --threshold 80 --fail-on error

# Review PR diff against audit
gh pr diff $PR_NUMBER | vertaa patch-review --job $JOB_ID

# Generate PR comment
vertaa comment --input results.json --format markdown
```

### Per-category thresholds

```yaml
# .vertaaux.yml or action input
thresholds:
  usability: 75
  accessibility: 85
  clarity: 70
  conversion: 60
```

---

## Remediation Workflow

**Goal:** Systematically fix issues from an audit.

### Step 1: Triage

```bash
vertaa audit https://example.com --mode deep --wait --format json > audit.json
cat audit.json | vertaa triage --verbose
```

Output: P0/P1/P2 priority buckets with effort estimates.

### Step 2: Plan

```bash
cat audit.json | vertaa fix-plan --json
```

Output: Ordered remediation steps with dependencies.

### Step 3: Fix

```bash
# Fix one issue at a time
vertaa fix <job-id>

# Or generate all fixes
vertaa fix-all <job-id>
```

### Step 4: Verify

```bash
vertaa verify
```

### Step 5: Document

```bash
# Generate team playbook for recurring issues
cat audit.json | vertaa doc --team "Frontend" --format markdown

# Generate release notes from before/after
vertaa compare --before baseline.json --after current.json
vertaa diff --job-a $BEFORE --job-b $AFTER --json | vertaa release-notes
```

---

## AI Agent Integration

**Goal:** Let AI agents (Claude, custom) run audits programmatically.

### Via MCP Server

Add to Claude Desktop `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vertaaux": {
      "url": "https://vertaaux.ai/mcp",
      "headers": { "X-API-Key": "vtx_..." }
    }
  }
}
```

MCP tools available: `create_audit`, `get_audit`, `get_quota`.

MCP findings include AI-optimized fields: `structured_fix`, `fixability`, `recommended_fix`.

### Via SDK in agent code

```typescript
import { createVertaauxClient } from "@vertaaux/sdk";

const client = createVertaauxClient({ apiKey: process.env.VERTAAUX_API_KEY! });

// Agent creates audit
const { job_id } = await client.createAudit({ url: targetUrl, mode: "standard" });

// Poll until complete
let result;
do {
  result = await client.getAudit(job_id);
  if (result.status !== "completed") await new Promise(r => setTimeout(r, 5000));
} while (result.status !== "completed");

// Agent processes results
const errorIssues = result.issues.filter(i => i.severity === "error");
const mechanicalFixes = result.issues.filter(i => i.fixability === "mechanical");
```

### Via CLI with machine mode

```bash
# Machine-readable JSON output (stdout = data, stderr = diagnostics)
vertaa audit https://example.com --wait --machine --format json 2>/dev/null

# Pipe through agent processing
vertaa audit https://example.com --machine --format json 2>/dev/null | agent-process
```

---

## Multi-Page Site Audit

**Goal:** Audit multiple pages of a site systematically.

### CLI approach

```bash
URLS=(
  "https://example.com"
  "https://example.com/pricing"
  "https://example.com/features"
  "https://example.com/signup"
  "https://example.com/docs"
)

for url in "${URLS[@]}"; do
  echo "Auditing $url..."
  vertaa audit "$url" --mode standard --wait --format json >> all-results.jsonl
done
```

### SDK approach (parallel)

```typescript
const urls = [
  "https://example.com",
  "https://example.com/pricing",
  "https://example.com/signup",
];

// Start all audits in parallel
const jobs = await Promise.all(
  urls.map(url => client.createAudit({ url, mode: "standard" }))
);

// Poll all until complete
const results = await Promise.all(
  jobs.map(async ({ job_id }) => {
    let result;
    do {
      result = await client.getAudit(job_id);
      if (result.status !== "completed") await new Promise(r => setTimeout(r, 3000));
    } while (result.status !== "completed");
    return result;
  })
);
```

---

## WCAG Compliance Report

**Goal:** Generate a WCAG 2.2 compliance report for stakeholders.

```bash
# Deep accessibility audit with markdown report
vertaa a11y https://example.com --mode deep --format md > wcag-report.md

# Add AI explanation and triage
vertaa a11y https://example.com --mode deep --format json > a11y.json
cat a11y.json | vertaa explain --verbose > explanation.md
cat a11y.json | vertaa triage > triage.md

# Generate team playbook for remediation
cat a11y.json | vertaa doc --team "Accessibility" --format markdown > playbook.md
```

### Findings structure for compliance mapping

Each finding maps to WCAG criteria:
- `wcagCriteria`: e.g., `"1.4.3"` (Contrast), `"2.1.1"` (Keyboard), `"4.1.2"` (Name, Role, Value)
- `ruleId`: engine-specific rule identifier
- `impact`: `critical`/`serious`/`moderate`/`minor` (a11y-specific; mapped to severity `error`/`warning`/`info`)
- `fixability`: helps estimate remediation effort
- `structured_fix`: provides machine-actionable fix operations
