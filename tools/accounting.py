"""Recompute the report's Section 11 budget from the raw records (run on the host; stdlib only).

    python accounting.py OUT.json

Inputs (private, not redistributed): the proxy's metering ledger (state dir proxy-data/ledger.db — copied first, read
only), the D'Agapeyeff task and chat-thread ids (exported from the agent board), the developer's Claude Code session
transcript, and the lab job records. Output: aggregates only — no prompts, keys or personal data.
"""
import collections
import glob
import json
import os
import shutil
import sqlite3
import sys
import tempfile
from datetime import datetime

# Paths come from the environment, so no machine-specific details are stored in this file:
#   PEGASUS_STATE_DIR   the platform's state directory (holds proxy-data/ledger.db and lab/jobs)
#   PEGASUS_WORKSPACE   the workspace holding .pegasus/dag_tasks.json and .pegasus/dag_threads.json
#   CLAUDE_TRANSCRIPT   the developer's Claude Code session transcript (.jsonl)
STATE = os.environ["PEGASUS_STATE_DIR"]
WS = os.environ["PEGASUS_WORKSPACE"]
TRANSCRIPT = os.environ["CLAUDE_TRANSCRIPT"]
START = "2026-10-09T00:41"          # first D'Agapeyeff task, as recorded by the platform (UTC)


def ledger(out):
    tmp = tempfile.mkdtemp()
    for f in glob.glob(os.path.join(STATE, "proxy-data", "ledger.db*")):
        shutil.copy(f, tmp)
    c = sqlite3.connect(os.path.join(tmp, "ledger.db"))
    tasks = set(json.load(open(os.path.join(WS, ".pegasus", "dag_tasks.json"))))
    threads = set(json.load(open(os.path.join(WS, ".pegasus", "dag_threads.json"))))
    rows = c.execute("select ts, amount_usd, agent_id, task_id, thread_id, model, input_tokens, cached_tokens, "
                     "output_tokens from entries where kind='cost' and ts >= '2026-10-07'").fetchall()

    def agg(rs, key):
        a = collections.defaultdict(lambda: {"calls": 0, "input": 0, "cached": 0, "output": 0, "usd": 0.0})
        for ts, usd, ag, tk, th, m, i, ca, o in rs:
            k = key(ts, ag, m)
            a[k]["calls"] += 1; a[k]["input"] += i or 0; a[k]["cached"] += ca or 0
            a[k]["output"] += o or 0; a[k]["usd"] = round(a[k]["usd"] + (usd or 0), 6)
        return dict(a)
    tr = [r for r in rows if r[3] in tasks]
    out["agents_on_tasks"] = agg(tr, lambda *_: "total")["total"]
    out["agents_by_model"] = agg(tr, lambda ts, ag, m: m)
    out["agents_by_day_utc"] = agg(tr, lambda ts, ag, m: ts[:10])
    out["agents_by_agent"] = agg(tr, lambda ts, ag, m: ag)
    out["planning_chat"] = agg([r for r in rows if r[4] in threads], lambda *_: "total").get("total")
    out["task_count"], out["thread_count"] = len(tasks), len(threads)


def claude(out):
    seen = {}
    with open(TRANSCRIPT, encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            if d.get("type") == "assistant" and m.get("usage") and d.get("timestamp", "") >= START:
                seen[m.get("id") or d.get("uuid")] = (m.get("model"), m["usage"])
    t = collections.Counter()
    models = collections.Counter()
    for model, u in seen.values():
        models[model] += 1
        for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens", "output_tokens"):
            t[k] += u.get(k) or 0
    out["developer_claude"] = {"api_calls": len(seen), "models": dict(models), **t,
                               "billing": "Claude Pro subscription, extra usage disabled (no per-token charge)"}


def lab(out):
    gpu_h = cpu_h = 0.0
    n = g = 0
    states = collections.Counter()
    for f in glob.glob(os.path.join(STATE, "lab", "jobs", "*", "status.json")):
        s = json.load(open(f))
        if not s.get("started_at") or not s.get("finished_at") or s.get("submitted_at", "") < START:
            continue
        h = (datetime.fromisoformat(s["finished_at"]) - datetime.fromisoformat(s["started_at"])).total_seconds() / 3600
        n += 1; states[s.get("state")] += 1
        if s.get("gpu"):
            g += 1; gpu_h += h
        else:
            cpu_h += h
    out["lab"] = {"jobs": n, "gpu_jobs": g, "gpu_hours": round(gpu_h, 1), "cpu_job_hours": round(cpu_h, 1),
                  "states": dict(states), "hardware": "laptop, NVIDIA GeForce RTX 5060 (8 GB)"}


if __name__ == "__main__":
    out = {"study": "D'Agapeyeff", "from": START[:10] + " (UTC)", "generated": datetime.now().date().isoformat()}
    ledger(out); claude(out); lab(out)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
    a = out["agents_on_tasks"]; d = out["developer_claude"]
    print(f"agents {a['calls']} calls ${a['usd']:.2f} | claude {d['api_calls']} calls | lab {out['lab']}")
