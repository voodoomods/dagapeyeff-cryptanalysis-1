"""Gather the validation run into one folder and write validation-results.json (machine-readable record).

    python validation/collect_results.py VALDIR WORKLAB OUTDIR
      VALDIR   the run's /val directory (logs/, flatness/, F66/, recompute_extra.json, compare.json, f68 log)
      WORKLAB  the working copy's lab/cipher (the rerun outputs)
      OUTDIR   destination (docs/validation-2026-10-16/ in the repository)

Copies, never moves: the run directory is left as it was. Records commands, exit codes and elapsed seconds from the
step logs, and the SHA-256 of every file copied.
"""
import hashlib, json, shutil, sys
from pathlib import Path

VAL, WORK, OUT = (Path(x) for x in sys.argv[1:4])
F68_DIR = Path(sys.argv[4]) if len(sys.argv) > 4 else None
OUT.mkdir(parents=True, exist_ok=True)
RERUN = {"grille/bench-2.json": "F71", "grille/bench-ngram.json": "F78", "grille/bench-tolerance.json": "F74",
         "round11/validate.json": "I47", "round11/identifiability-A-val.json": "F76", "round11/identifiability-B-val.json": "F76",
         "round12/ident-val.json": "F77", "round12/comparability-val.json": "F79",
         "round11/micro-digraph-cells.json": "R35", "round11/micro-digraph-cells-4x5.json": "R35",
         "round12/fsq-val.json": "O34", "round12/fsq-order.json": "O34"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


files = []


def take(src, rel, claim=""):
    if not src.exists():
        return
    dst = OUT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    files.append({"path": rel, "bytes": dst.stat().st_size, "sha256": sha(dst), **({"claim": claim} if claim else {})})


for rel, claim in RERUN.items():
    take(WORK / rel, f"rerun/{rel}", claim)
for f in sorted((VAL / "logs").glob("*")):
    take(f, f"logs/{f.name}")
for f in sorted((VAL / "flatness").glob("*.json")):
    take(f, f"flatness/{f.name}", "F31/F80/F81")
for f in sorted((VAL / "F66" / "reps").glob("rep*")):
    take(f, f"f66/{f.name}", "F66")
take(VAL / "recompute_extra.json", "recompute_extra.json", "F4/F32/R29")
take(VAL / "recompute_extra.log", "logs/recompute_extra.log")
take(VAL / "compare.json", "compare.json")
if F68_DIR:
    take(F68_DIR / "power-rerun.json", "f68/power-rerun.json", "F68")
    take(F68_DIR / "power-rerun.cfg.json", "f68/power-rerun.cfg.json", "F68")

steps = []
for f in sorted((VAL / "logs").glob("steps-*.jsonl")):
    for line in f.read_text().splitlines():
        if line.startswith("{"):
            steps.append(json.loads(line))
cmp_ = json.loads((VAL / "compare.json").read_text()) if (VAL / "compare.json").exists() else {}
env = json.loads((VAL / "env.json").read_text()) if (VAL / "env.json").exists() else {}
record = {
    "validation_date": "2026-10-16",
    "release_candidate": {"repository": "voodoomods/dagapeyeff-cryptanalysis", "commit": "44f7b233d76744e98b5ed164d4144a93f6f0cd0d",
                          "branch": "main", "manifest_check": "130/130 files OK (sha256sum -c MANIFEST.sha256 on a fresh clone)"},
    "performed_by": "the project's developer (Claude Opus 5.5) at the author's request - internal, not independent replication",
    "environment": env,
    "steps": steps,
    "totals": {"steps": len(steps), "exit_nonzero": sum(s["exit"] != 0 for s in steps),
               "seconds": sum(s["seconds"] for s in steps)},
    "comparison_summary": cmp_.get("summary"),
    "checks": [{k: c.get(k) for k in ("id", "kind", "claim", "status", "source_inspection", "reason", "note") if c.get(k) is not None}
               for c in cmp_.get("checks", [])],
    "failures": [c["id"] for c in cmp_.get("checks", []) if c["status"] in ("FAIL",)],
    "not_run": [c["id"] for c in cmp_.get("checks", []) if c["status"] == "NOT RUN"],
    "files": files,
}
(OUT / "validation-results.json").write_text(json.dumps(record, indent=1))
print(json.dumps(record["totals"]), record["comparison_summary"], len(files), "files")
