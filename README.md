# OpenClaw Knowledge Factory

A reusable system to turn continuous intel reports into durable knowledge and executable upgrades.

## Why

Fast research loops create many notes, but value is lost without curation and application.
This project standardizes a full pipeline:

1. Ingest findings from intel briefs
2. Score and filter by relevance and confidence
3. Distill into knowledge cards
4. Convert cards into implementation playbooks
5. Track adoption outcomes and feedback

## Core Outcomes

- `dist/knowledge_index.json`: machine-readable index of scored findings
- `dist/action_backlog.md`: ranked application tasks
- Reusable templates for cards and playbooks

## Quick Start

```bash
cd /home/admin/.openclaw/workspace/projects/openclaw-knowledge-factory
python3 scripts/build_index.py \
  --reports-dir ../openclaw-intel-lab/reports \
  --out-json dist/knowledge_index.json \
  --out-backlog dist/action_backlog.md
```

## Suggested Weekly Cadence

- Daily: run ingestion/index build
- Every 2 days: promote top findings into knowledge cards
- Weekly: execute top 3 playbooks and record impact
- Monthly: prune low-value cards and refresh scoring weights

## Repo Layout

- `KNOWLEDGE_SYSTEM_DESIGN.md`: operating model and governance
- `principles/`: stable, reusable principles
- `playbooks/`: executable application guides
- `cases/`: adoption and impact records
- `guides/`: setup guides (network skills, codex workflow, qmd memory, cron-heartbeat orchestration, github sharing)
- `scripts/build_index.py`: report parser and scorer
- `templates/knowledge_card.md`: normalized knowledge artifact
- `templates/apply_playbook.md`: implementation template
- `dist/`: generated outputs

## Share to Other OpenClaw Nodes

1. Push this repo to GitHub
2. In each OpenClaw workspace, add it as a git submodule or clone it
3. Wire scheduled runs (cron/heartbeat) to execute `build_index.py`
4. Consume `action_backlog.md` as the default execution queue
