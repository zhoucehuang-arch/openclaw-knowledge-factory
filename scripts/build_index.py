#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

DOMAINS = {
    "评估": "evaluation",
    "安全": "security",
    "成本": "cost",
    "记忆": "memory",
    "多智能体": "workflow",
    "界面": "ux",
    "治理": "security",
}


def infer_domain(text: str) -> str:
    for k, v in DOMAINS.items():
        if k in text:
            return v
    return "workflow"


def score_item(text: str) -> dict:
    relevance = 4 if any(k in text for k in ["OpenClaw", "Agent", "智能体"]) else 3
    confidence = 4 if "http" in text else 3
    leverage = 4 if any(k in text for k in ["框架", "治理", "评估", "成本"]) else 3
    cost = 3
    transferability = 4
    priority = round(0.30 * relevance + 0.25 * confidence + 0.25 * leverage + 0.10 * cost + 0.10 * transferability, 2)
    return {
        "relevance": relevance,
        "confidence": confidence,
        "leverage": leverage,
        "cost": cost,
        "transferability": transferability,
        "priority": priority,
    }


def extract_findings(md: str):
    findings = []
    in_a = False
    for line in md.splitlines():
        if line.startswith("## A"):
            in_a = True
            continue
        if in_a and line.startswith("## ") and not line.startswith("## A"):
            break
        if in_a:
            m = re.match(r"^\d+\.\s+\*\*(.+?)\*\*", line.strip())
            if m:
                findings.append(m.group(1))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reports-dir", required=True)
    ap.add_argument("--out-json", required=True)
    ap.add_argument("--out-backlog", required=True)
    args = ap.parse_args()

    reports_dir = Path(args.reports_dir)
    records = []

    for report in sorted(reports_dir.glob("*-intel-brief.md")):
        text = report.read_text(encoding="utf-8", errors="ignore")
        for finding in extract_findings(text):
            scores = score_item(finding)
            records.append(
                {
                    "report": str(report),
                    "finding": finding,
                    "domain": infer_domain(finding),
                    **scores,
                }
            )

    records.sort(key=lambda x: x["priority"], reverse=True)

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    backlog_lines = ["# Action Backlog", ""]
    for i, rec in enumerate(records[:20], start=1):
        backlog_lines.append(
            f"{i}. [{rec['domain']}] {rec['finding']}  (priority={rec['priority']}, source={Path(rec['report']).name})"
        )

    out_backlog = Path(args.out_backlog)
    out_backlog.parent.mkdir(parents=True, exist_ok=True)
    out_backlog.write_text("\n".join(backlog_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
