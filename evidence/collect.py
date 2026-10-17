"""Collect the evidence for the D'Agapeyeff findings into this folder — re-runnable (each run refreshes the copies and
rewrites MANIFEST.md). Run inside the agent container:

    python /workspace/research/cipher/dagapeyeff/evidence/collect.py

What it gathers (copies, never moves): the case file snapshot, every lab results file and the script that produced it,
the engine versions those scripts imported, each lab job's status record, the write-ups (findings, novelty check,
briefings). MANIFEST.md lists every file with its SHA-256 and maps each case entry to the files that support it, so a
reader can check that the numbers in the report are the numbers the runs produced.
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/app")
HERE = Path(__file__).resolve().parent
LAB = Path("/lab/cipher")
WS = Path("/workspace/research/cipher/dagapeyeff")

# case entry -> (lab results, producing script, lab job ids)
CLAIMS = {
    "F71": (["grille/bench-2.json"], ["grille/bench2.py"], ["20261014-002920-eb8a"]),
    "F73": (["grille/bench-ngram.json"], ["grille/bench_ngram.py"], ["20261014-013414-0e0e"]),
    "F78": (["grille/bench-ngram.json"], ["grille/bench_ngram.py"], ["20261014-013414-0e0e"]),
    "F74": (["grille/bench-tolerance.json"], ["grille/bench_tolerance.py"], ["20261014-023519-9bce"]),
    "I47": (["round11/validate.json", "round11/identifiability-A.json", "round11/identifiability-B.json",
             "round11/identifiability-A-big.json", "round11/identifiability-B-big.json"],
            ["round11/table_test.py", "round11/identifiability.py"],
            ["20261014-032058-a3e9", "20261014-042657-5f13", "20261014-042657-225c",
             "20261014-042944-11e7", "20261014-042944-5d7d"]),
    "F75": ([], [], []),
    "R34": (["round11/micro-digraph-cells.json", "round11/micro-digraph-cells-4x5.json"],
            ["round11/micro_digraph_cells.py", "round11/micro_digraph_cells_4x5.py"], []),
    "R35": (["round11/micro-digraph-cells.json", "round11/micro-digraph-cells-4x5.json"],
            ["round11/micro_digraph_cells.py", "round11/micro_digraph_cells_4x5.py"], []),
    "F77": (["round12/ident-full.json", "round12/ident-small.json"], ["round12/review_checks.py"],
            ["20261015-103450-384b", "20261015-102809-7942"]),
    "F79": (["round12/comparability.json"], ["round12/comparability.py"], ["20261015-153404-0b85"]),
    "F80": (["provenance/latin_flatness.json"], ["provenance/latin_flatness.py"], []),
    "O34": (["round12/fsq-full.json", "round12/fsq-order.json"], ["round12/review_checks.py", "round12/fsq_order.py"],
            ["20261015-103450-9ade", "20261015-135503-fc9c"]),
    "O33": (["round12/fsq-full.json", "round12/fsq-small.json", "round12/fsq-order.json"],
            ["round12/review_checks.py", "round12/fsq_order.py"],
            ["20261015-103450-9ade", "20261015-102809-72d7", "20261015-135503-fc9c"]),
}
ENGINES = ["grille/grille_engine.py", "grille/poly_engine.py", "grille/digraph_engine.py"]
DOCS = ["FINDINGS.md", "literature/NOVELTY-CHECK-2026-10-14.md", "literature/novelty-search-2026-10-14.json",
        "BRIEFING-round10.md", "literature/gariazzo2026/Report_Agapeyeff.pdf",
        "literature/hendrick2026/paper/dagapeyeff-exclusions.pdf"]
EXTRA = {"F75": ["/workspace/.pegasus/kahn_snippets.json"]}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def copy(src: Path, dest_rel: str, rows: list):
    if not src.exists():
        rows.append((dest_rel, "MISSING", str(src)))
        return
    dst = HERE / dest_rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    rows.append((dest_rel, sha(dst), str(src)))


def main():
    rows: list = []
    from app import case_file as cf
    from app import case_graph as g
    rec = cf.load("dagapeyeff")
    (HERE / "case").mkdir(exist_ok=True)
    (HERE / "case" / "dagapeyeff.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False), encoding="utf-8")
    rows.append(("case/dagapeyeff.json", sha(HERE / "case" / "dagapeyeff.json"), "case_file.load('dagapeyeff')"))

    from app import lab_tools as lt
    jobs = {}
    for cid, (results, scripts, job_ids) in CLAIMS.items():
        for r in results:
            copy(LAB / r, f"results/{r}", rows)
        for s in scripts:
            copy(LAB / s, f"scripts/{s}", rows)
        for j in job_ids:
            try:
                st = lt._call("GET", f"/jobs/{j}")
            except Exception as e:  # noqa: BLE001
                st = {"error": str(e)}
            jobs[j] = st
        for x in EXTRA.get(cid, []):
            copy(Path(x), f"sources/{Path(x).name}", rows)
    (HERE / "jobs").mkdir(exist_ok=True)
    (HERE / "jobs" / "lab_jobs.json").write_text(json.dumps(jobs, indent=1, default=str), encoding="utf-8")
    rows.append(("jobs/lab_jobs.json", sha(HERE / "jobs" / "lab_jobs.json"), "lab /jobs/{id} status records"))
    for e in ENGINES:
        copy(LAB / e, f"engines/{e}", rows)
    for d in DOCS:
        copy(WS / d, f"docs/{d}", rows)

    by_id = {e["id"]: e for e in rec["entries"]}
    lines = ["# Evidence manifest — D'Agapeyeff", "",
             f"Generated {datetime.now(timezone.utc).isoformat()} by `evidence/collect.py`. Every file below is a copy; SHA-256 lets a reader confirm it is the file the claim cites.", "",
             "## Claims → evidence", ""]
    for cid, (results, scripts, job_ids) in CLAIMS.items():
        e = by_id.get(cid, {})
        risk = g.at_risk(rec, cid) if e else []
        lines += [f"### {cid} — {e.get('status', 'missing')}{' · AT RISK: ' + ', '.join(risk) if risk else ''}",
                  f"> {e.get('text', '(not in case file)')}", "",
                  f"- evidence (case file): {e.get('evidence', '')}"]
        lines += [f"- result: `results/{r}`" for r in results] + [f"- script: `scripts/{s}`" for s in scripts]
        lines += [f"- lab job: `{j}` — {(jobs.get(j) or {}).get('state', '?')}" for j in job_ids]
        lines += [f"- source: `sources/{Path(x).name}`" for x in EXTRA.get(cid, [])] + [""]
    lines += ["## Files", "", "| file | sha256 | copied from |", "|---|---|---|"]
    lines += [f"| `{a}` | `{b[:16]}…` | {c} |" if b != "MISSING" else f"| `{a}` | **MISSING** | {c} |"
              for a, b, c in rows]
    (HERE / "MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(rows)} files; missing: {[a for a, b, _ in rows if b == 'MISSING']}")


if __name__ == "__main__":
    main()
