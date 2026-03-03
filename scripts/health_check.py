#!/usr/bin/env python3
import argparse
import json
import sys
import time
from pathlib import Path


def load_json(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"missing file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def age_seconds(ts):
    if ts is None:
        return None
    try:
        return int(time.time() - float(ts))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description="Check orchestration health for cron/heartbeat/qmd memory")
    ap.add_argument("--state", required=True, help="path to heartbeat-state.json")
    ap.add_argument("--max-cron-age-hours", type=int, default=14)
    ap.add_argument("--max-close-loop-gap", type=float, default=0.95)
    ap.add_argument("--max-duplicate-notify-rate", type=float, default=0.10)
    args = ap.parse_args()

    state = load_json(Path(args.state))
    issues = []

    cron_jobs = state.get("cronJobs", {})
    max_age = args.max_cron_age_hours * 3600

    for name, job in cron_jobs.items():
        age = age_seconds(job.get("lastSuccess"))
        if age is None:
            issues.append(f"{name}: no lastSuccess timestamp")
            continue
        if age > max_age:
            issues.append(f"{name}: stale success age={age}s > {max_age}s")

        if not job.get("lastReportPath"):
            issues.append(f"{name}: missing lastReportPath")

        if job.get("status") not in {"ok", "warning", "error", "unknown"}:
            issues.append(f"{name}: invalid status={job.get('status')}")

    metrics = state.get("metrics", {})
    close_loop = metrics.get("closeLoopRate24h")
    dup_rate = metrics.get("duplicateNotifyRate24h")
    missed = metrics.get("missedDelivery24h")

    if close_loop is not None and close_loop < args.max_close_loop_gap:
        issues.append(f"closeLoopRate24h too low: {close_loop} < {args.max_close_loop_gap}")

    if dup_rate is not None and dup_rate > args.max_duplicate_notify_rate:
        issues.append(f"duplicateNotifyRate24h too high: {dup_rate} > {args.max_duplicate_notify_rate}")

    if missed is not None and missed > 0:
        issues.append(f"missedDelivery24h non-zero: {missed}")

    result = {
        "ok": len(issues) == 0,
        "issues": issues,
        "checkedAt": int(time.time()),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if issues:
        sys.exit(2)


if __name__ == "__main__":
    main()
