"""Provenance check (2026-10-16): the Latin figure of case F31 ('a deliberately balanced table matches the cipher's
flatness in 368 of 1,000 Latin windows'), and its dependence on which Latin texts are sampled.

Runs the committed F31 tool (flatness_tools.frequency_flatness, PegasusDMZ agent image, commit 8c4e0fa) — so it needs
the agent container (/app), like the original computation; it is not reproducible from this repository alone.

  1. As committed: the tool's default call (as for F31), and Latin alone on seeds 0-3 (full 10-edition corpus,
     lines that are mostly English filtered out).
  2. Latin from the six editions without English apparatus only (files below), same filter, seeds 0-3.
  3. English-marker share of each Latin stream.

    python latin_flatness.py   ->  /lab/cipher/provenance/latin_flatness.json
"""
import json, re, sys
sys.path.insert(0, "/app")
from app import cryptanalysis_tools as ct, flatness_tools as ft

CLEAN = {"augustine-confessiones.txt", "caesar-bello-gallico.txt", "cicero-orations.txt", "descartes-meditationes.txt",
         "newton-principia.txt", "virgil-aeneid.txt"}
EN = {"THE", "AND", "OF", "TO", "IS", "WAS", "THAT", "WHICH", "WITH", "HE", "HIS", "IT", "FOR", "AS", "BY", "THIS", "BE",
      "NOT", "ARE"}


def marker(lines):
    w = [x.upper() for ws in lines for x in ws]
    return round(100 * sum(x in EN for x in w) / len(w), 2), len(w)


if len(sys.argv) > 1 and sys.argv[1] == "clean":
    d = ct._corpus_dir("la")

    def only_clean(code):
        rows = []
        for f in sorted(d.glob("*.txt")):
            if f.name not in CLEAN:
                continue
            for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
                ws = [w for w in (ct._fold(x) for x in re.split(r"[^\w]+", line)) if w]
                if ws and sum(w in ct._EN_FUNCTION for w in ws) / len(ws) < 0.2:
                    rows.append(ws)
        return tuple(rows)
    ct._corpus_lines = only_clean
    text = ct._corpus_text("la")
    res = {"marker": marker(only_clean("la")), "letters": len(text),
           "by_seed": {s: json.loads(ft.frequency_flatness.invoke({"languages": "la", "windows": 1000, "seed": s}))
                       ["comparison"]["la"]["as_flat_best_balanced_table"] for s in range(4)}}
    print(json.dumps(res))
    sys.exit(0)

out = {"tool": "flatness_tools.frequency_flatness (windows=1000)"}
r = json.loads(ft.frequency_flatness.invoke({"windows": 1000, "seed": 0}))     # the tool's default call, as for F31
out["default_call_seed0"] = {k: v["as_flat_best_balanced_table"] for k, v in r["comparison"].items()}
out["full_latin_by_seed"] = {s: json.loads(ft.frequency_flatness.invoke({"languages": "la", "windows": 1000, "seed": s}))
                             ["comparison"]["la"]["as_flat_best_balanced_table"] for s in range(4)}
out["full_latin_stream_english_marker_pct_words"] = marker(ct._corpus_lines("la"))

def clean_run():
    """Separate process: the six editions only, restricted BEFORE anything loads (the tools cache their streams)."""
    import subprocess
    r = subprocess.run([sys.executable, __file__, "clean"], capture_output=True, text=True, check=True)
    return json.loads(r.stdout.strip().splitlines()[-1])


if len(sys.argv) > 1 and sys.argv[1] == "clean":
    pass
else:
    c = clean_run()
    out["clean_six_english_marker_pct_words"] = c["marker"]
    out["clean_six_letters"] = c["letters"]
    out["clean_six_by_seed"] = c["by_seed"]
json.dump(out, open("/lab/cipher/provenance/latin_flatness.json", "w"), indent=1)
print(json.dumps(out, indent=1))
