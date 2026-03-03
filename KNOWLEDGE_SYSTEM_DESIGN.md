# Knowledge System Design

## 1) Problem

Continuous intel collection is effective for discovery but weak for retention and execution.
Primary failure modes:

- report flood (too many items, weak prioritization)
- novelty bias (new > useful)
- no closed-loop adoption tracking
- weak transferability across OpenClaw instances

## 2) Design Goals

- Convert streams into reusable, versioned knowledge
- Prioritize by practical value, not hype
- Tie every key insight to a concrete action
- Provide portable artifacts for other OpenClaw deployments

## 3) Artifact Model

Each insight should end in one of three artifact types:

1. `Signal`: a new observation with evidence
2. `Principle`: stable rule extracted from repeated signals
3. `Playbook`: executable implementation guide

Promotion flow:

`Signal -> Principle -> Playbook`

## 4) Evaluation Rubric (0-5)

- **Relevance**: fit to OpenClaw goals
- **Confidence**: source quality + cross-source agreement
- **Leverage**: expected impact if applied
- **Cost**: implementation complexity/time (inverse score)
- **Transferability**: can be reused by other nodes

Priority score:

`priority = 0.30*relevance + 0.25*confidence + 0.25*leverage + 0.10*cost + 0.10*transferability`

## 5) Filtering Rules

Keep only items that satisfy all rules:

- at least one concrete source URL
- includes a testable claim or pattern
- maps to an OpenClaw subsystem (workflow, security, evaluation, cost, ux, memory)

Reject items if:

- purely trend/opinion with no actionable mechanism
- duplicate claim already in knowledge base
- cost is high and leverage is low

## 6) Application Protocol

For top-ranked items:

1. Create a `knowledge_card`
2. Define one measurable experiment (owner, metric, deadline)
3. Execute in constrained scope first
4. Record outcome (win/neutral/fail + evidence)
5. Update score based on real-world result

## 7) Governance

- Weekly review: merge duplicates, retire stale cards
- Monthly refactor: update taxonomy and scoring weights
- Keep an immutable changelog for major principle updates

## 8) GitHub Sharing Standard

Recommended public repo sections:

- `principles/`: stable cross-node rules
- `playbooks/`: implementation recipes
- `adoption-cases/`: before/after impact reports
- `templates/`: reusable card/playbook templates

Contribution checklist:

- cite sources
- define applicability boundary
- include failure modes
- include rollback path

## 9) First 30-Day Execution Plan

- Week 1: bootstrap index + backlog from existing reports
- Week 2: promote top 10 signals into cards
- Week 3: execute top 3 playbooks in production-like environment
- Week 4: publish impact summary and refine rubric
