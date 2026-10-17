"""Compare the clean-room reproduction (run_repro.sh, run from a fresh copy of the repository with no network) with the
published results, run by run. Writes repro-compare.json beside this file.

    python compare_repro.py            (paths relative to the repository's lab/cipher/)
"""
import json
from pathlib import Path

C = Path(__file__).resolve().parents[2]          # lab/cipher
R = Path(__file__).resolve().parent              # lab/cipher/round12/repro
L = lambda p: json.loads(p.read_text())           # noqa: E731
out = {}

a = {(r["plant"], r["n"]): r["orbits_up_to_rotation"] for r in L(C / "grille/bench-ngram.json")["runs"]}
b = {(r["plant"], r["n"]): r["orbits_up_to_rotation"] for r in L(R / "bench-ngram-repro.json")["runs"]}
out["F78_grille_benchmark"] = {"runs": len(a), "same_orbits": sum(a[k] == b[k] for k in a)}

for c in "AB":
    pub = {(r["plant"], r["L"]): r for r in L(C / f"round11/identifiability-{c}-big.json")["runs"] if r["start"] == "truth"}
    rep = [r for r in L(R / f"identifiability-{c}-repro.json")["runs"] if r["start"] == "truth"]
    out[f"F76_corpus_{c}"] = {"runs": len(rep),
                              "same_outcome": sum(pub[(r["plant"], r["L"])]["wrong_found"] == r["wrong_found"] for r in rep)}

key = lambda r: (r["exp"], r["model"], r["source"], r["plant"], r["L"])  # noqa: E731
pub = {key(r): r for r in L(C / "round12/ident-full.json")["runs"]}
rep = L(R / "ident-repro.json")["runs"]
out["F77_robustness"] = {"runs": len(rep), "same_outcome": sum(pub[key(r)]["wrong_found"] == r["wrong_found"] for r in rep)}

pub = {r["window"]: r["min_cells"] for r in L(C / "round12/fsq-full.json")["runs"]}
rep = L(R / "fsq-repro.json")["runs"]
out["O33_purpose_built_four_square"] = {"passages": len(rep), "same_min_cells": sum(pub[r["window"]] == r["min_cells"] for r in rep)}
out["O33_order_test_summary_identical"] = L(C / "round12/fsq-order.json")["summary"] == L(R / "fsq-order-repro.json")["summary"]

# Field-level: every recorded field except elapsed time ("seconds"), and whole-file byte identity.
def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in ("seconds", "mean_seconds")}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def fields(pub, rep, key):
    P = {key(r): strip(r) for r in L(C / pub)["runs"]}
    Rr = [strip(r) for r in L(R / rep)["runs"]]
    return {"records": len(Rr), "identical_except_timing": sum(P[key(r)] == r for r in Rr)}


out["field_level"] = {
    "bench-ngram": {"identical_except_timing": strip(L(C / "grille/bench-ngram.json")) == strip(L(R / "bench-ngram-repro.json")),
                    "bytes_identical": (C / "grille/bench-ngram.json").read_bytes() == (R / "bench-ngram-repro.json").read_bytes()},
    "identifiability-A": fields("round11/identifiability-A-big.json", "identifiability-A-repro.json", lambda r: (r["plant"], r["L"], r["start"])),
    "identifiability-B": fields("round11/identifiability-B-big.json", "identifiability-B-repro.json", lambda r: (r["plant"], r["L"], r["start"])),
    "ident-full": fields("round12/ident-full.json", "ident-repro.json", key),
    "fsq-full": fields("round12/fsq-full.json", "fsq-repro.json", lambda r: r["window"]),
    "fsq-order": {"bytes_identical": (C / "round12/fsq-order.json").read_bytes() == (R / "fsq-order-repro.json").read_bytes()},
}
(R / "repro-compare.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
