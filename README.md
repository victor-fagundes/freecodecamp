# Knowledge Work Plugins for Cursor

Anthropic's [knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) installed and adapted for Cursor Agent Skills.

## What's installed

- **Source plugins** live in `knowledge-work-plugins/` (first-party Anthropic plugins; Apache-2.0).
- **Cursor skills** live in `.cursor/skills/` — Agent discovers these automatically.
- **MCP stubs** live in `.cursor/mcp.json` — enable and authenticate the connectors you use.

## How to use

1. Open Agent chat and type `/` to see skills (e.g. `/write-spec`, `/roadmap-update`, `/brainstorm`).
2. Or just ask naturally — "write a PRD for SSO" should pick up `write-spec`.
3. Connect tools in **Customize → MCP** (Linear, Notion, Slack, Figma, etc.). Skills use `~~category` placeholders and work without connectors if you paste context.

## Product management (recommended start)

| Skill | Use when |
|---|---|
| `write-spec` | PRD / feature spec |
| `roadmap-update` | Roadmap create / reprioritize |
| `stakeholder-update` | Weekly / exec updates |
| `synthesize-research` | Interview / survey synthesis |
| `pm-competitive-brief` | Competitor analysis |
| `metrics-review` | Product metrics review |
| `product-brainstorming` / `brainstorm` | Thinking partner |
| `sprint-planning` | Sprint planning |

## Adaptations for Cursor

- Skills flattened into `.cursor/skills/<name>/` (Cursor discovery format).
- Name collisions renamed: `pm-competitive-brief`, `mkt-competitive-brief`, `sales-lead-triage`, `smb-lead-triage`, `bio-research-start`, `productivity-start`.
- `CONNECTORS.md` copied next to each skill that needs it (`references/CONNECTORS.md`).
- Claude Code / Cowork install commands removed from the project README; MCP OAuth client IDs stripped (Cursor handles OAuth).
- Partner-built plugins omitted (install separately if needed).

## Customize for your company

Edit skill files under `.cursor/skills/` to add your terminology, process, and templates. Prefer editing there (what Cursor loads) over `knowledge-work-plugins/` (upstream mirror).

## Re-sync after upstream updates

Replace `knowledge-work-plugins/` with a newer first-party checkout, then run:

```bash
python3 scripts/sync-cursor-skills.py
```

## Skills by plugin

- **bio-research**: `bio-research-start`, `instrument-data-to-allotrope`, `nextflow-development`, `scientific-problem-selection`, `scvi-tools`, `single-cell-rna-qc`
- **cowork-plugin-management**: `cowork-plugin-customizer`, `create-cowork-plugin`
- **customer-support**: `customer-escalation`, `customer-research`, `draft-response`, `kb-article`, `ticket-triage`
- **data**: `analyze`, `build-dashboard`, `create-viz`, `data-context-extractor`, `data-visualization`, `explore-data`, `sql-queries`, `statistical-analysis`, `validate-data`, `write-query`
- **design**: `accessibility-review`, `design-critique`, `design-handoff`, `design-system`, `research-synthesis`, `user-research`, `ux-copy`
- **engineering**: `architecture`, `code-review`, `debug`, `deploy-checklist`, `documentation`, `incident-response`, `standup`, `system-design`, `tech-debt`, `testing-strategy`
- **enterprise-search**: `digest`, `knowledge-synthesis`, `search`, `search-strategy`, `source-management`
- **finance**: `audit-support`, `close-management`, `financial-statements`, `journal-entry`, `journal-entry-prep`, `reconciliation`, `sox-testing`, `variance-analysis`
- **human-resources**: `comp-analysis`, `draft-offer`, `interview-prep`, `onboarding`, `org-planning`, `people-report`, `performance-review`, `policy-lookup`, `recruiting-pipeline`
- **legal**: `brief`, `compliance-check`, `legal-response`, `legal-risk-assessment`, `meeting-briefing`, `review-contract`, `signature-request`, `triage-nda`, `vendor-check`
- **marketing**: `brand-review`, `campaign-plan`, `content-creation`, `draft-content`, `email-sequence`, `mkt-competitive-brief`, `performance-report`, `seo-audit`
- **operations**: `capacity-plan`, `change-request`, `compliance-tracking`, `process-doc`, `process-optimization`, `risk-assessment`, `runbook`, `status-report`, `vendor-review`
- **pdf-viewer**: `view-pdf`
- **product-management**: `brainstorm`, `metrics-review`, `pm-competitive-brief`, `product-brainstorming`, `roadmap-update`, `sprint-planning`, `stakeholder-update`, `synthesize-research`, `write-spec`
- **productivity**: `memory-management`, `productivity-start`, `task-management`, `update`
- **sales**: `account-context`, `account-plan`, `account-research`, `account-tiering`, `call-prep`, `call-summary`, `close-plan`, `competitive-intelligence`, `create-an-asset`, `crm-hygiene-check`, `customer-health`, `customer-voice`, `daily-briefing`, `deal-advance-gap`, `deal-review`, `deal-signals`, `deal-slip-scenario`, `draft-outreach`, `end-of-day`, `expansion-whitespace`, `forecast`, `handle-objection`, `inbox-sweep`, `log-activity`, `pipeline-review`, `renewal-radar`, `rep-context`, `route-lead`, `sales-lead-triage`, `schedule-meeting`, `setup`, `stakeholder-map`, `team-pipeline`, `update-opportunity`, `weekly-wrap`, `win-loss-review`
- **small-business**: `ad-manager`, `ap-processor`, `brand-style`, `build-agent`, `build-connector`, `business-pulse`, `call-list`, `canva-creator`, `cash-flow-snapshot`, `close-month`, `content-strategy`, `contract-review`, `crm-autopilot`, `grant-rfp-writer`, `grow-pipeline`, `growth-pulse`, `hiring-screener`, `inbox-manager`, `inventory-planner`, `invoice-chase`, `job-post-builder`, `lead-finder`, `marketing-monday`, `monday-brief`, `month-end-prep`, `outreach-composer`, `pay-the-bills`, `payroll-prep`, `plan-payroll`, `proposal-builder`, `reactivate`, `report-builder`, `report-pack`, `restock`, `review-reputation`, `seo-ai-visibility`, `smb-lead-triage`, `smb-onboard`, `smb-router`, `social-content-engine`, `speed-to-lead`, `tax-prep`, `tax-season-organizer`, `ticket-deflector`

