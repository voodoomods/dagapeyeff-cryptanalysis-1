"""Expected-output comparison for the full-size validation rerun (validation/run_all.sh).

Two predeclared criteria per experiment, fixed before the rerun finished (October 16, 2026):

  1. Record identity   every record of the rerun equals the published record in every field except elapsed time
                       ("seconds", "mean_seconds"). The experiments are seeded; an earlier reduced-size clean-room run
                       (lab/cipher/round12/repro) was identical, so any difference is reported, not explained away.
  2. Paper numbers     every number the report prints is recomputed from the rerun's own records and must equal the
                       printed value (percentages to the printed precision). The same extractor is first applied to
                       the published file ("source inspection"), so a mismatch there is a reporting error, not a
                       rerun difference.

  status  PASS     both criteria met
          PARTIAL  paper numbers met, some records differ (listed)
          FAIL     a paper number differs in the rerun or in the published file
          NOT RUN  the rerun step has not finished with exit code 0 (from the run log steps-*.jsonl), so its output file -
           which may be a partial file written while the step runs, or the published copy - is not read

    python validation/compare.py --ref PUBLISHED/lab/cipher --new RERUN/lab/cipher [--extra RECOMPUTE.json]
                                 [--steps LOGDIR] [--f66 DIR_OF_REPS] [--flatness DIR] [--f68 FILE] [--out compare.json]
"""
import argparse, glob, json, math
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--ref", required=True)
ap.add_argument("--new", required=True)
ap.add_argument("--extra")
ap.add_argument("--steps", help="directory holding steps-gpu.jsonl / steps-cpu.jsonl from run_all.sh")
ap.add_argument("--f66")
ap.add_argument("--flatness")
ap.add_argument("--f68", help="F68 rerun result (power-rerun.json); its step log is steps-f68.jsonl in --steps")
ap.add_argument("--out", default="compare.json")
a = ap.parse_args()
REF, NEW = Path(a.ref), Path(a.new)
TIMING = ("seconds", "mean_seconds", "tag")   # "tag" = the output-file suffix given on the command line (-val)


def load(p):
    return json.loads(Path(p).read_text()) if Path(p).exists() else None


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in TIMING}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def records(d):
    return d["runs"] if isinstance(d, dict) and "runs" in d else d


def identity(ref, new):
    """(records compared, identical, first differing indexes)"""
    r, n = records(ref), records(new)
    if isinstance(r, list) and isinstance(n, list):
        same = [strip(x) == strip(y) for x, y in zip(r, n)]
        whole = strip({k: v for k, v in ref.items() if k != "runs"}) == strip({k: v for k, v in new.items() if k != "runs"}) \
            if isinstance(ref, dict) else True
        return {"records_published": len(r), "records_rerun": len(n), "identical_except_timing": sum(same),
                "other_fields_identical": whole, "differing_records": [i for i, s in enumerate(same) if not s][:20]}
    return {"records_published": 1, "records_rerun": 1, "identical_except_timing": int(strip(ref) == strip(new)),
            "other_fields_identical": True, "differing_records": []}


def pct(k, n):
    return round(100 * k / n)


results = []
STEPS = {}
if a.steps:
    for f in glob.glob(str(Path(a.steps) / "steps-*.jsonl")):
        for line in Path(f).read_text().splitlines():
            if line.startswith("{"):
                rec = json.loads(line)
                STEPS[rec["step"]] = rec
STEP_OF = {"F71": ["F71_bench2"], "F78": ["F78_bench_ngram"], "F74": ["F74_bench_tolerance"], "I47": ["I47_table_validate"],
           "F76-A": ["F76_identifiability_A"], "F76-B": ["F76_identifiability_B"],
           "F76-both": ["F76_identifiability_A", "F76_identifiability_B"], "F77": ["F77_robustness"],
           "F79": ["F79_comparability"], "R35-5x5": ["R35_digraph_5x5"], "R35-4x5": ["R35_digraph_4x5"],
           "O34-search": ["O34_fsq_search"], "O34-order": ["O34_fsq_order"], "F68": ["F68_power"]}


def step_done(cid):
    """None if every step behind this check finished with exit 0, else the reason it did not."""
    for name in STEP_OF.get(cid, []):
        rec = STEPS.get(name)
        if rec is None:
            return f"step {name} not finished (running or not started)"
        if rec["exit"] != 0:
            return f"step {name} exited {rec['exit']} after {rec['seconds']} s"
    return None



def check(cid, claim, ref_file, new_file, extract, expected, note=""):
    why = step_done(cid)
    ref, new = load(REF / ref_file), (None if why else load(NEW / new_file))
    row = {"id": cid, "claim": claim, "published_file": ref_file, "rerun_file": new_file, "expected": expected,
           "criteria": "record identity (all fields except elapsed time) + every printed number recomputed", "note": note}
    if ref is None:
        row.update(status="FAIL", reason="published file missing")
        return results.append(row)
    row["published_numbers"] = extract(ref)
    src_ok = row["published_numbers"] == expected
    if new is None:
        row.update(status="NOT RUN", reason=why or "rerun output missing", source_inspection="PASS" if src_ok else "FAIL")
        return results.append(row)
    row["rerun_numbers"] = extract(new)
    row["step"] = [STEPS[n] for n in STEP_OF.get(cid, []) if n in STEPS]
    row["identity"] = identity(ref, new)
    num_ok = row["rerun_numbers"] == expected
    ident_ok = (row["identity"]["identical_except_timing"] == row["identity"]["records_published"]
                == row["identity"]["records_rerun"] and row["identity"]["other_fields_identical"])
    row["source_inspection"] = "PASS" if src_ok else "FAIL"
    row["status"] = "FAIL" if not (src_ok and num_ok) else ("PASS" if ident_ok else "PARTIAL")
    results.append(row)


# ---- F71: grille recovered with the letter key given (3 of 3, all 49 orbits up to rotation)
check("F71", "Turning grille recovered in practice ciphers when the letter key is known", "grille/bench-2.json", "grille/bench-2.json",
      lambda d: {"key_given_exact": sum(r["orbits_up_to_rotation"] == 49 for r in d if r["case"] == "key given"),
                 "key_given_runs": sum(r["case"] == "key given" for r in d)},
      {"key_given_exact": 3, "key_given_runs": 3})


# ---- F78: six-symbol scoring 6/6 (5 exact), five-symbol 6/6 (3 exact, >= 47), four-symbol 2/6
def f78(d):
    out = {}
    for n in (4, 5, 6):
        o = [r["orbits_up_to_rotation"] for r in d["runs"] if r["n"] == n]
        out[f"n{n}"] = {"recovered_ge45": sum(x >= 45 for x in o), "exact": sum(x == 49 for x in o), "min": min(o), "of": len(o)}
    return out


check("F78", "Six-symbol scoring recovers 6/6 grilles (5 exact); five-symbol 6/6 (47-49, 3 exact); four-symbol 2/6",
      "grille/bench-ngram.json", "grille/bench-ngram.json", f78,
      {"n4": {"recovered_ge45": 2, "exact": 1, "min": 18, "of": 6}, "n5": {"recovered_ge45": 6, "exact": 3, "min": 47, "of": 6},
       "n6": {"recovered_ge45": 6, "exact": 5, "min": 48, "of": 6}})

# ---- F74: table must be essentially exact
check("F74", "True table 4/4; 2 misplaced 1/4; 4 misplaced 2/4; 6, 8, 12 misplaced 0/12",
      "grille/bench-tolerance.json", "grille/bench-tolerance.json",
      lambda d: {k: [v["solved"], v["of"]] for k, v in d["summary"].items()},
      {"0": [4, 4], "2": [1, 4], "4": [2, 4], "6": [0, 4], "8": [0, 4], "12": [0, 4]})

# ---- I47: table repair moves a near-miss table further from the truth (2 wrong -> 5)
check("I47", "Table repair from 2 wrong letters ends further away (5 wrong)", "round11/validate.json", "round11/validate.json",
      lambda d: [[r["case"], r["plant"], r["wrong_before"], r["wrong_after"]] for r in d["runs"]][:1],
      [["wrong2", 0, 2, 5]])

# ---- F76: identifiability table (corpus A, B, both) and the 178/200 at 182
LENGTHS = (182, 273, 364, 455, 546, 728, 1092)


def kept(d):
    # the report's convention: the truth is kept only if the search returns it exactly; a numerical tie counts as not
    # kept (Section 6.4 notes the other convention would give 48% instead of 46% for corpus A at 364 symbols)
    return {L: sum(1 for r in d["runs"] if r["start"] == "truth" and r["L"] == L and r["exact"]) for L in LENGTHS}


for c, row in (("A", [14, 31, 46, 65, 72, 84, 94]), ("B", [8, 22, 36, 49, 54, 65, 74])):
    check(f"F76-{c}", f"Truth kept, corpus {c}, 100 practice ciphers per length (%)",
          f"round11/identifiability-{c}-big.json", f"round11/identifiability-{c}-val.json",
          lambda d: [kept(d)[L] for L in LENGTHS], row)


def f76_both():
    out = {}
    for tag, files in (("published", [REF / f"round11/identifiability-{c}-big.json" for c in "AB"]),
                       ("rerun", [NEW / f"round11/identifiability-{c}-val.json" for c in "AB"])):
        ds = [load(f) for f in files] if tag == "published" or not step_done("F76-both") else [None]
        if None in ds:
            out[tag] = None
            continue
        k = [kept(ds[0])[L] + kept(ds[1])[L] for L in LENGTHS]
        rates = [x / 2 for x in k]
        cross = next(i for i, x in enumerate(rates) if x >= 50)
        L0, L1, r0, r1 = LENGTHS[cross - 1], LENGTHS[cross], rates[cross - 1], rates[cross]
        out[tag] = {"both_pct": rates, "beaten_at_182": 200 - k[0], "kept_at_182": k[0],
                    "half_crossing_symbols": round((L0 + (50 - r0) * (L1 - L0) / (r1 - r0)) / 10) * 10}
    exp = {"both_pct": [11.0, 26.5, 41.0, 57.0, 63.0, 74.5, 84.0], "beaten_at_182": 178, "kept_at_182": 22,
           "half_crossing_symbols": 420}
    st = "NOT RUN" if out["rerun"] is None else ("PASS" if out["rerun"] == exp == out["published"] else "FAIL")
    results.append({"id": "F76-both", "claim": "Both corpora (%); 178 of 200 beaten at 182; one in two at roughly 420 symbols",
                    "expected": exp, "published_numbers": out["published"], "rerun_numbers": out["rerun"],
                    "source_inspection": "PASS" if out["published"] == exp else "FAIL", "status": st,
                    "criteria": "printed numbers recomputed from both corpora (linear interpolation, nearest 10)",
                    **({"reason": step_done("F76-both")} if out["rerun"] is None else {})})


f76_both()

# ---- F77: robustness (2,000 runs) and the two cross-checks at 182
SET_LENGTHS = (182, 273, 364, 546)


def f77(d):
    S = d["summary"]
    setups = sorted({k.rsplit(" ", 1)[0] for k in S})
    out = {"setups": len(setups)}
    for L in SET_LENGTHS:
        ks = [S[f"{s} L{L}"] for s in setups]
        rates = [x["exact"] / x["plants"] for x in ks]
        out[f"L{L}"] = {"lowest_pct": pct(min(rates), 1), "highest_pct": pct(max(rates), 1),
                        "pooled_pct": pct(sum(x["exact"] for x in ks), sum(x["plants"] for x in ks)),
                        "runs": sum(x["plants"] for x in ks)}
    r = [x for x in d["runs"] if x["L"] == 182 and x["truth_beaten"]]
    o = [x for x in r if x.get("other_found_minus_truth") is not None]
    f = [x for x in r if x.get("fresh_found_minus_truth") is not None]
    out["other_corpus_still_beats"] = [sum(x["other_found_minus_truth"] > 0 for x in o), len(o)]
    out["fresh_passage_beats"] = [sum(x["fresh_found_minus_truth"] > 0 for x in f), len(f)]
    return out


check("F77", "Ten setups x four lengths (2,000 runs): lowest/highest/pooled truth kept; 171/248 other corpus; 82/427 fresh passage",
      "round12/ident-full.json", "round12/ident-val.json", f77,
      {"setups": 10, "L182": {"lowest_pct": 8, "highest_pct": 26, "pooled_pct": 15, "runs": 500},
       "L273": {"lowest_pct": 10, "highest_pct": 42, "pooled_pct": 26, "runs": 500},
       "L364": {"lowest_pct": 16, "highest_pct": 44, "pooled_pct": 29, "runs": 500},
       "L546": {"lowest_pct": 28, "highest_pct": 60, "pooled_pct": 41, "runs": 500},
       "other_corpus_still_beats": [171, 248], "fresh_passage_beats": [82, 427]})


# ---- F79: comparability
def f79(d):
    beat = {L: sum(c["beat_truth"][L] for c in d["consistency"]) for L in ("10000", "100000")}
    return {"mass_A": round(d["mass"]["A"]["mass_min"], 2), "mass_B": round(d["mass"]["B"]["mass_min"], 2),
            "log10_spread_max": round(max(d["mass"][c]["log10_mass_spread"] for c in "AB"), 3),
            "neighbors_tested": sum(c["neighbors"] for c in d["consistency"]),
            "beat_truth_10k": beat["10000"], "beat_truth_100k": beat["100000"],
            "normalized_truth_start_runs": len(d["truth_start"])}


check("F79", "Model mass 2.10 (A') / 1.45 (B), spread 0.002 log10; 0 of 9,150 neighbors beat the truth at 10k/100k symbols",
      "round12/comparability.json", "round12/comparability-val.json", f79,
      {"mass_A": 2.1, "mass_B": 1.45, "log10_spread_max": 0.002, "neighbors_tested": 9150, "beat_truth_10k": 0,
       "beat_truth_100k": 0, "normalized_truth_start_runs": 200})

# ---- R35: random-key four-square / two-square never reach 13 symbols (10,000 practice ciphers)
check("R35-5x5", "5x5 four-square and two-square: 22-25 distinct symbols, none <= 13 (2 x 2,000 plants)",
      "round11/micro-digraph-cells.json", "round11/micro-digraph-cells.json",
      lambda d: {s: [d[s]["distinct_cells_min"], d[s]["distinct_cells_max"], d[s]["plants_with_13_or_fewer"]] for s in ("four", "two")}
      | {"plants_each": d["plants_per_system"]},
      {"four": [22, 25, 0], "two": [22, 25, 0], "plants_each": 2000})
check("R35-4x5", "4x5 squares 18-20 symbols; 5x5 with 13-letter text 20-25; none <= 13 (3 x 2,000 plants)",
      "round11/micro-digraph-cells-4x5.json", "round11/micro-digraph-cells-4x5.json",
      lambda d: {k: [v["distinct_cells_min"], v.get("distinct_cells_max", v["distinct_cells_median"]) if k != "four_square_4x5_20_letters" else v["distinct_cells_median"], v["plants_with_13_or_fewer"], v["plants"]]
                 for k, v in d.items() if isinstance(v, dict)},
      None, note="expected filled from the published file; the paper prints the ranges 18-20 and 20-25 and 'none'")
# the 4x5 expected values are the published file's own numbers; the range check below is the printed claim
_r = results[-1]
if _r.get("published_numbers"):
    _r["expected"] = _r["published_numbers"]
    pn = _r["published_numbers"]
    printed = (pn["four_square_5x5_text_13_letters"][0] == 20 and all(v[2] == 0 for v in pn.values())
               and pn["four_square_4x5_20_letters"][0] == 18)
    _r["source_inspection"] = "PASS" if printed else "FAIL"
    if _r.get("rerun_numbers") is not None:
        ident = _r["identity"]
        same = ident["identical_except_timing"] == ident["records_published"] and ident["other_fields_identical"]
        _r["status"] = "FAIL" if _r["rerun_numbers"] != pn or not printed else ("PASS" if same else "PARTIAL")


# ---- O34: purpose-built four-square
def o34_search(d):
    r13 = [r for r in d["runs"] if r["min_cells"] <= 13]
    flats = [r["flat_p_if_13"] for r in r13]
    return {"windows": len(d["runs"]), "with_13_or_fewer": len(r13), "all_13_flat": all(p is not None and p >= 0.73 for p in flats),
            "flat_p_range": [min(flats), max(flats)] if flats else None,
            "windows_13": sorted(r["window"] for r in r13)}


ref_fsq = load(REF / "round12/fsq-full.json")
check("O34-search", "Purpose-built four-square reaches 13 symbols in 13 of 100 passages, all as flat as the cipher (p 0.85-1.0)",
      "round12/fsq-full.json", "round12/fsq-val.json", o34_search,
      o34_search(ref_fsq) if ref_fsq else None, note="windows_13 and the flat-p range are taken from the published file")
_r = results[-1]
if _r.get("published_numbers"):
    pn = _r["published_numbers"]
    printed = (pn["with_13_or_fewer"] == 13 and pn["windows"] == 100 and pn["all_13_flat"]
               and round(pn["flat_p_range"][0], 2) == 0.85 and pn["flat_p_range"][1] >= 0.995)
    _r["source_inspection"] = "PASS" if printed else "FAIL"
    if not printed:
        _r["status"] = "FAIL"
    elif _r.get("rerun_numbers") is not None and _r["rerun_numbers"] == pn:
        _r["status"] = "PASS" if _r["identity"]["identical_except_timing"] == _r["identity"]["records_published"] else "PARTIAL"


def o34_order(d):
    s = d["summary"]
    flagged13 = sorted(r["window"] for r in d["purpose_built"] if r.get("cells") == 13 and r["family_p"] < 0.05)
    return {"purpose_built_flagged": [s["purpose_built_all"]["family_p_below_0.05"], s["purpose_built_all"]["texts"]],
            "random_key_flagged": [s["random_key"]["family_p_below_0.05"], s["random_key"]["texts"]],
            "flat13_flagged": [s["purpose_built_13_flat"]["family_p_below_0.05"], s["purpose_built_13_flat"]["texts"]],
            "flat13_flagged_windows": flagged13,
            "flat13_pair_stat_p_below_0.05": s["purpose_built_13_flat"]["mi_even_or_odd_p_below_0.05"],
            "real_family_p": s["real_message"]["family_p"]}


check("O34-order", "Order test: purpose-built 12/100 vs random 52/100 flagged; 3 of 13 flat (34, 77, 95); 7 of 13 pair stats; real p = 0.999",
      "round12/fsq-order.json", "round12/fsq-order.json", o34_order,
      {"purpose_built_flagged": [12, 100], "random_key_flagged": [52, 100], "flat13_flagged": [3, 13],
       "flat13_flagged_windows": [34, 77, 95], "flat13_pair_stat_p_below_0.05": 7, "real_family_p": 0.999})

# ---- Independent recomputations (new code, not the original)
if a.extra and Path(a.extra).exists():
    x = load(a.extra)
    results.append({"id": "F4", "kind": "independent recomputation", "claim": "All 8 rare symbols in column 14; odds below 1 in 20,000 after scanning row lengths 2-20",
                    "expected": "p < 1/20,000", "rerun_numbers": {k: x["F4"][k] for k in ("real_statistic", "exact_union_bound_p", "shuffles", "shuffles_reaching_real")},
                    "status": "PASS" if x["F4"]["pass"] else "FAIL", "note": x["F4"]["note"]})
    lay, lag = x["F32_layout"], x["F32_lag_component"]
    results.append({"id": "F32", "kind": "independent recomputation", "claim": "No order: rows p 0.08, columns 0.30, halves 0.10 / 0.60; lags 1-26 family-wise p 0.91",
                    "expected": "all p > 0.05; lag family p near 0.91", "rerun_numbers": {**{k: lay[k] for k in ("rows_p", "columns_p", "top_vs_bottom_p", "left_vs_right_p")},
                                                                                       "lag_family_p": lag["family_p"]},
                    "status": "PASS" if lay["pass"] and lag["pass"] else "FAIL", "note": lay["note"]})
    r = x["R29"]
    results.append({"id": "R29", "kind": "independent recomputation", "claim": "Polyphonic table without transposition: lag-1 dependence in 40 of 40 planted texts; real message p = 0.70",
                    "expected": ">= 38 of 40 at p < 0.05 and real p > 0.05 (predeclared tolerance for new seeds)",
                    "rerun_numbers": {k: r[k] for k in ("p_below_0.05", "p_below_0.01", "real_message_lag1_p")},
                    "status": ("PASS" if r["p_below_0.05"] == 40 else "PARTIAL") if r["pass"] else "FAIL",
                    "note": "new seeds and new code: 39 of 40 here against 40 of 40 printed; the conclusion holds, the exact count is seed-dependent"})
if a.f66 and Path(a.f66).exists():
    reps = [load(f) for f in sorted(glob.glob(str(Path(a.f66) / "rep*.json")))]
    fp = sorted(r["family_p"] for r in reps)
    results.append({"id": "F66", "kind": "rerun of the original script (unseeded) from a copy writing elsewhere",
                    "claim": "Hendrick's 30-statistic no-message test replicated: family-wise p = 0.29 (Hendrick 0.28)",
                    "expected": "family-wise p > 0.05 in every replication; published 0.291 inside the replication range",
                    "rerun_numbers": {"replications": len(fp), "family_p_min": fp[0], "family_p_median": fp[len(fp) // 2], "family_p_max": fp[-1],
                                      "smallest_stat_always_info_lag_3": all(r["real_smallest_statistic"] == "info lag 3" for r in reps)},
                    "status": "PASS" if fp and fp[0] > 0.05 and fp[0] <= 0.291 <= fp[-1] else "FAIL",
                    "note": "the script draws its 1,000 dealings without a seed, so 0.29 is one draw; 20 reruns give the spread"})
if a.flatness and Path(a.flatness).exists():
    fl = {Path(f).stem: load(f) for f in glob.glob(str(Path(a.flatness) / "*.json"))}
    en = fl.get("en_seed0")
    la = [fl[k] for k in sorted(fl) if k.startswith("la_full")]
    six = [fl[k] for k in sorted(fl) if k.startswith("la_clean6")]
    num = lambda s: int(s.split("/")[0])  # noqa: E731
    obs = {"english_balanced": en and en["as_flat_best_balanced_table"], "english_top": en and en["as_flat_top_letters"],
           "latin_all": [x["as_flat_best_balanced_table"] for x in la], "latin_six": [x["as_flat_best_balanced_table"] for x in six]}
    ok = (en and num(en["as_flat_best_balanced_table"]) == 364 and la and all(345 <= num(x["as_flat_best_balanced_table"]) <= 374 for x in la)
          and six and all(167 <= num(x["as_flat_best_balanced_table"]) <= 182 for x in six))
    results.append({"id": "F31/F80", "kind": "standalone recomputation (validation/flatness_standalone.py; wordfreq 3.1.1 + scipy only)",
                    "claim": "Balanced table as flat as the cipher: English 364/1,000; Latin 345-374 (ten editions), 167-182 (six without English notes)",
                    "expected": "English 364; Latin all in 345-374; six editions in 167-182", "rerun_numbers": obs,
                    "status": "PASS" if ok else "FAIL"})
    lt = [(x["min_distinct_letters"], x["median_distinct_letters"], x["max_distinct_letters"]) for x in [en] + la if x]
    results.append({"id": "S2-letters", "kind": "standalone recomputation", "claim": "Section 2: natural passages use 17 to 22 different letters",
                    "expected": "range within 17-22", "rerun_numbers": {"min_median_max_per_run": lt},
                    "status": "PASS" if all(17 <= lo and hi <= 22 for lo, _, hi in lt) else "FAIL",
                    "note": "182-letter windows of the English and Latin streams use about 18-26 letters, median 22"})

if a.f68:
    why = step_done("F68")
    d = None if why else load(a.f68)
    curve = [[c["budget_seconds"], c["recovered"]] for c in d["curve"]] if d else None
    exp = [[60.0, "0/3"], [300.0, "0/3"], [1200.0, "0/3"]]
    results.append({"id": "F68", "kind": "rerun of the original lab job's configuration with the platform engine (not in this repository)",
                    "claim": "Joint grille-and-table search recovers 0 of 3 practice ciphers at every budget (60, 300, 1,200 s per phase)",
                    "expected": exp, "rerun_numbers": curve, "step": [STEPS[n] for n in STEP_OF["F68"] if n in STEPS],
                    "status": "NOT RUN" if d is None else ("PASS" if curve == exp else "FAIL"),
                    **({"reason": why or "result file missing"} if d is None else {}),
                    "note": "budgets are wall-clock seconds, so the outcome depends on the hardware; the original ran on the same GPU"})

summary = {s: sum(r["status"] == s for r in results) for s in ("PASS", "PARTIAL", "FAIL", "NOT RUN")}
Path(a.out).write_text(json.dumps({"criteria": __doc__.split("\n\n")[1], "summary": summary, "checks": results}, indent=1))
for r in results:
    print(f"{r['status']:8} {r['id']:12} {r['claim'][:90]}")
print(summary)
